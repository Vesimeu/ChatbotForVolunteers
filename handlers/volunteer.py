from aiogram import types
from aiogram.dispatcher import Dispatcher

from ChatbotForVolunteers.handlers.events import show_events
from ChatbotForVolunteers.handlers.organizations import show_organizations
from ChatbotForVolunteers.handlers.participant import subscribe_to_newsletter

async def show_volunteer_chat(message: types.Message):
    await message.answer("Присоединяйтесь к чату волонтёров: [ссылка на чат]")

def register_volunteer_handlers(dp: Dispatcher):
    dp.register_message_handler(show_volunteer_chat, text="Общение с волонтёрами")
    dp.register_message_handler(show_organizations, text="Информация про эко-организации")
    dp.register_message_handler(show_events, text="Календарь мероприятий")
    dp.register_message_handler(subscribe_to_newsletter, text="Подписаться на рассылку")
