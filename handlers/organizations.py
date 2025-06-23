from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from service.organization_service import (
    get_all_organizations, create_organization, delete_organization,
    get_organization_by_id, update_organization
)


# 📌 Состояния FSM для организации
class OrganizationState(StatesGroup):
    waiting_for_edit_id = State()
    waiting_for_name = State()
    waiting_for_description = State()
    waiting_for_contact = State()
    waiting_for_website = State()


async def show_organizations(message: types.Message):
    """
    Обработчик для показа списка организаций с описанием.
    """
    organizations = await get_all_organizations()

    if organizations:
        response = "🌿 Список эко-организаций:\n\n"
        for org in organizations:
            response += (
                f"🏛 <b>{org.name}</b>\n"
                f"🆔 ID: {org.id}\n"
                f"📝 <i>{org.description}</i>\n"
                f"🌍 Сайт: {org.website if org.website else 'нет'}\n"
                f"📞 Контакты: {org.contact_info}\n"
                f"────────────────────\n\n"
            )
    else:
        response = "❌ Пока нет зарегистрированных эко-организаций."

    await message.answer(response, parse_mode="HTML")


# 📌 Создание организации
async def start_create_organization(message: types.Message):
    await message.answer("Введите название организации:")
    await OrganizationState.waiting_for_name.set()


async def process_org_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = message.text
    await message.answer("Введите описание организации:")
    await OrganizationState.waiting_for_description.set()


async def process_org_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["description"] = message.text
    await message.answer("Введите контактные данные организации:")
    await OrganizationState.waiting_for_contact.set()


async def process_org_contact(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["contact_info"] = message.text
    await message.answer("Введите сайт организации (если нет, напишите 'нет'):")
    await OrganizationState.waiting_for_website.set()


async def process_org_website(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        website = None if message.text.lower() == "нет" else message.text
        organization = await create_organization(
            name=data["name"],
            description=data["description"],
            contact_info=data["contact_info"],
            website=website
        )
    await message.answer(f"✅ Организация '{organization.name}' создана.")
    await state.finish()


# 📌 Удаление организации
async def start_delete_organization(message: types.Message):
    """
    Показывает список организаций для удаления.
    """
    organizations = await get_all_organizations()
    if not organizations:
        await message.answer("❌ Нет организаций для удаления.")
        return

    response = "🗑 Введите ID организации для удаления:\n"
    response += "\n".join([f"🆔 {org.id} | {org.name}" for org in organizations])
    await message.answer(response)

    await OrganizationState.waiting_for_edit_id.set()


async def process_delete_organization(message: types.Message, state: FSMContext):
    """
    Удаляет выбранную организацию.
    """
    org_id = message.text.strip()
    if not org_id.isdigit():
        await message.answer("⚠ Введите корректный ID.")
        return

    success = await delete_organization(int(org_id))
    if success:
        await message.answer("✅ Организация удалена.")
    else:
        await message.answer("❌ Организация не найдена.")

    await state.finish()


def register_organization_handlers(dp: Dispatcher):
    """
    Регистрация обработчиков для работы с организациями.
    """
    dp.register_message_handler(show_organizations, text="Список организаций")
    dp.register_message_handler(start_create_organization, text="Создать организацию")
    dp.register_message_handler(process_org_name, state=OrganizationState.waiting_for_name)
    dp.register_message_handler(process_org_description, state=OrganizationState.waiting_for_description)
    dp.register_message_handler(process_org_contact, state=OrganizationState.waiting_for_contact)
    dp.register_message_handler(process_org_website, state=OrganizationState.waiting_for_website)
    dp.register_message_handler(start_delete_organization, text="Удалить организацию")
    dp.register_message_handler(process_delete_organization, state=OrganizationState.waiting_for_edit_id)
