from aiogram import types
from aiogram.dispatcher import Dispatcher
from ChatbotForVolunteers.service.event_service import get_all_events
from ChatbotForVolunteers.service.user_service import update_subscription_status

async def show_events(message: types.Message):
    events = await get_all_events()
    if events:
        response = "Список мероприятий:\n" + "\n".join([f"{event.name} - {event.date}" for event in events])
    else:
        response = "Мероприятий пока нет."
    await message.answer(response)

async def subscribe_to_newsletter(message: types.Message):
    success = await update_subscription_status(message.from_user.id, True)
    await message.answer("Вы подписались на рассылку!" if success else "Сначала зарегистрируйтесь через /start.")

def register_participant_handlers(dp: Dispatcher):
    dp.register_message_handler(show_events, text="Календарь мероприятий")
    dp.register_message_handler(subscribe_to_newsletter, text="Подписаться на рассылку")
