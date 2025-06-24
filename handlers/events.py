from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from datetime import datetime
from database import get_db
from service.event_service import (
    get_all_events, create_event, delete_event, get_event_by_id, update_event
)
from service.organization_service import get_all_organizations, get_organization_by_id
from service.user_service import get_user_by_telegram_id
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from service.volunteer_service import subscribe_volunteer_to_event, get_volunteers_for_event


# 📌 Состояния FSM для мероприятия
class EventState(StatesGroup):
    waiting_for_edit_id = State()
    waiting_for_organization_id = State()
    waiting_for_name = State()
    waiting_for_date = State()
    waiting_for_description = State()
    waiting_for_location = State()
    waiting_for_contact_info = State()
    waiting_for_volunteers_needed = State()

async def show_events(message: types.Message):
    """
    Обработчик для показа списка мероприятий с кнопками в зависимости от роли.
    """
    user = await get_user_by_telegram_id(message.from_user.id)
    if not user:
        await message.answer("❌ Вы не зарегистрированы. Пожалуйста, введите /start.")
        return

    events = await get_all_events()

    if not events:
        await message.answer("❌ Мероприятий пока нет.")
        return

    await message.answer("📅 **Список актуальных мероприятий:**")

    for event in events:
        organization_name = event.organization.name if event.organization else "Не указана"
        response = (
            f"📌 **Название:** {event.name}\n"
            f"📅 **Дата:** {event.date.strftime('%Y-%m-%d %H:%M')}\n"
            f"📍 **Место:** {event.location}\n"
            f"📜 **Описание:** {event.description}\n"
            f"📞 **Контакты:** {event.contact_info}\n"
            f"👥 **Требуется волонтёров:** {event.volunteers_needed}\n"
            f"🏢 **Организация:** {organization_name}\n"
        )

        keyboard = InlineKeyboardMarkup()
        if user.role == "volunteer":
            keyboard.add(InlineKeyboardButton("✅ Записаться", callback_data=f"subscribe_event_{event.id}"))
        elif user.role == "organizer":
             keyboard.add(InlineKeyboardButton("👥 Список волонтеров", callback_data=f"list_volunteers_{event.id}"))

        await message.answer(response, reply_markup=keyboard)


async def subscribe_to_event_callback(callback_query: types.CallbackQuery):
    """
    Обрабатывает нажатие на кнопку 'Записаться'.
    """
    event_id = int(callback_query.data.split("_")[2])
    user_id = callback_query.from_user.id

    # Получаем user.id из нашей базы, а не telegram_id
    user = await get_user_by_telegram_id(user_id)
    if not user:
        await callback_query.answer("❌ Ошибка: пользователь не найден.")
        return

    success = await subscribe_volunteer_to_event(user.id, event_id)

    if success:
        await callback_query.answer("✅ Вы успешно записались на мероприятие!")
    else:
        await callback_query.answer("ℹ️ Вы уже записаны на это мероприятие.", show_alert=True)


async def list_volunteers_callback(callback_query: types.CallbackQuery):
    """
    Обрабатывает нажатие на кнопку 'Список волонтеров'.
    """
    event_id = int(callback_query.data.split("_")[2])
    volunteers = await get_volunteers_for_event(event_id)

    if not volunteers:
        await callback_query.answer("👥 На это мероприятие еще никто не записался.", show_alert=True)
        return

    response = "👥 **Список волонтеров:**\n"
    for user in volunteers:
        response += f"- {user.username or f'User ID {user.telegram_id}'}\n"

    await callback_query.message.answer(response)
    await callback_query.answer()


# 📌 Создание мероприятия
async def start_create_event(message: types.Message):
    """
    Начинает процесс создания мероприятия.
    """
    organizations = await get_all_organizations()
    if not organizations:
        await message.answer("❌ Нет доступных организаций. Сначала создайте хотя бы одну.")
        return

    response = "📝 Выберите ID организации, к которой будет привязано мероприятие:\n"
    response += "\n".join([f"🆔 {org.id} | {org.name}" for org in organizations])
    await message.answer(response)

    await EventState.waiting_for_organization_id.set()


async def process_event_organization_id(message: types.Message, state: FSMContext):
    """
    Обрабатывает ID выбранной организации.
    """
    org_id = message.text.strip()
    if not org_id.isdigit():
        await message.answer("⚠ Введите корректный числовой ID организации.")
        return

    organization = await get_organization_by_id(int(org_id))
    if not organization:
        await message.answer("❌ Организация с таким ID не найдена. Попробуйте ещё раз.")
        return

    async with state.proxy() as data:
        data["organization_id"] = int(org_id)

    await message.answer("Введите название мероприятия:")
    await EventState.waiting_for_name.set()


async def process_event_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = message.text
    await message.answer("Введите дату мероприятия (ГГГГ-ММ-ДД ЧЧ:ММ):")
    await EventState.waiting_for_date.set()


async def process_event_date(message: types.Message, state: FSMContext):
    """
    Обрабатывает дату мероприятия и проверяет её корректность.
    """
    try:
        event_date = datetime.strptime(message.text, "%Y-%m-%d %H:%M")
    except ValueError:
        await message.answer("⚠ Некорректный формат! Введите дату в формате ГГГГ-ММ-ДД ЧЧ:ММ.")
        return

    async with state.proxy() as data:
        data["date"] = event_date

    await message.answer("Введите описание мероприятия:")
    await EventState.waiting_for_description.set()


async def process_event_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["description"] = message.text
    await message.answer("Введите место проведения мероприятия:")
    await EventState.waiting_for_location.set()


async def process_event_location(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["location"] = message.text
    await message.answer("Введите контактную информацию для мероприятия:")
    await EventState.waiting_for_contact_info.set()


async def process_event_contact_info(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["contact_info"] = message.text
    await message.answer("Введите количество необходимых волонтёров (число):")
    await EventState.waiting_for_volunteers_needed.set()


async def process_event_volunteers_needed(message: types.Message, state: FSMContext):
    """
    Завершает создание мероприятия и сохраняет его в базу данных.
    """
    async with state.proxy() as data:
        if not message.text.isdigit():
            await message.answer("⚠ Введите корректное число волонтёров.")
            return
        data["volunteers_needed"] = int(message.text)

    # Получаем пользователя из БД, чтобы использовать внутренний ID
    user = await get_user_by_telegram_id(message.from_user.id)
    if not user:
        await message.answer("❌ Ошибка: пользователь не найден. Попробуйте /start.")
        await state.finish()
        return

    async for session in get_db():  # ✅ Создаём асинхронную сессию
        event = await create_event(
            session=session,  # ✅ Передаём сессию в функцию
            name=data["name"],
            date=data["date"],
            description=data["description"],
            location=data["location"],
            contact_info=data["contact_info"],
            volunteers_needed=data["volunteers_needed"],
            organizer_id=user.id,  # ✅ ИСПРАВЛЕНО: передаем ID из базы данных
            organization_id=data["organization_id"]
        )

        await message.answer(f"✅ Мероприятие '{event.name}' успешно создано!")

    await state.finish()


# 📌 Удаление мероприятия
async def start_delete_event(message: types.Message):
    """
    Показывает список мероприятий для удаления.
    """
    events = await get_all_events()
    if not events:
        await message.answer("❌ Нет мероприятий для удаления.")
        return

    response = "🗑 Введите ID мероприятия для удаления:\n"
    response += "\n".join([f"🆔 {event.id} | {event.name}" for event in events])
    await message.answer(response)

    await EventState.waiting_for_edit_id.set()


async def process_delete_event(message: types.Message, state: FSMContext):
    """
    Удаляет выбранное мероприятие.
    """
    event_id = message.text.strip()
    if not event_id.isdigit():
        await message.answer("⚠ Введите корректный ID мероприятия.")
        return

    success = await delete_event(int(event_id))
    if success:
        await message.answer("✅ Мероприятие удалено.")
    else:
        await message.answer("❌ Мероприятие не найдено.")

    await state.finish()


def register_events_handlers(dp: Dispatcher):
    """
    Регистрация обработчиков для работы с мероприятиями.
    """
    dp.register_message_handler(show_events, text="Список мероприятий")

    # Создание мероприятия
    dp.register_message_handler(start_create_event, text="Создать мероприятие")
    dp.register_message_handler(process_event_organization_id, state=EventState.waiting_for_organization_id)
    dp.register_message_handler(process_event_name, state=EventState.waiting_for_name)
    dp.register_message_handler(process_event_date, state=EventState.waiting_for_date)
    dp.register_message_handler(process_event_description, state=EventState.waiting_for_description)
    dp.register_message_handler(process_event_location, state=EventState.waiting_for_location)
    dp.register_message_handler(process_event_contact_info, state=EventState.waiting_for_contact_info)
    dp.register_message_handler(process_event_volunteers_needed, state=EventState.waiting_for_volunteers_needed)

    # Удаление мероприятия
    dp.register_message_handler(start_delete_event, text="Удалить мероприятие")
    dp.register_message_handler(process_delete_event, state=EventState.waiting_for_edit_id)

    # Обработчики для инлайн-кнопок
    dp.register_callback_query_handler(subscribe_to_event_callback, lambda c: c.data.startswith('subscribe_event_'))
    dp.register_callback_query_handler(list_volunteers_callback, lambda c: c.data.startswith('list_volunteers_'))
