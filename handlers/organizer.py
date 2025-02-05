from aiogram import types
from aiogram.dispatcher import Dispatcher

from handlers.organizations import show_organizations, start_delete_organization
from handlers.events import show_events, start_delete_event
from service.user_service import get_user_by_telegram_id
from handlers.utils import get_keyboard_for_role


async def organizer_panel(message: types.Message):
    """
    Главное меню организатора.
    """
    user = await get_user_by_telegram_id(message.from_user.id)
    if not user or user.role != "organizer":
        await message.answer("⛔ У вас нет доступа.")
        return

    keyboard = get_keyboard_for_role(user.role)
    await message.answer("🔧 Панель организатора. Выберите действие:", reply_markup=keyboard)


def register_organizer_handlers(dp: Dispatcher):
    """
    Регистрация обработчиков для работы с организаторами.
    """
    dp.register_message_handler(organizer_panel, commands=["organizer"])

    # Работа с организациями
    dp.register_message_handler(show_organizations, text="Список организаций")
    dp.register_message_handler(start_delete_organization, text="Удалить организацию")

    # Работа с мероприятиями
    dp.register_message_handler(show_events, text="Список мероприятий")
    dp.register_message_handler(start_delete_event, text="Удалить мероприятие")
