from aiogram import types
from aiogram.dispatcher import Dispatcher
from ChatbotForVolunteers.service.event_service import get_all_events

async def show_events(message: types.Message):
    """
    Обработчик для показа списка мероприятий.
    """
    events = await get_all_events()

    if events:
        response = "Список мероприятий:\n"
        for event in events:
            response += f"{event.name} - {event.date}\n"
        await message.answer(response)
    else:
        await message.answer("Мероприятий пока нет.")

def register_events_handlers(dp: Dispatcher):
    """
    Регистрация обработчиков для работы с мероприятиями.
    """
    dp.register_message_handler(show_events, commands=["events"])
