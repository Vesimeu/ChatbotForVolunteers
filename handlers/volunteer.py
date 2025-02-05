from aiogram import types
from aiogram.dispatcher import Dispatcher

from handlers.events import show_events
from handlers.organizations import show_organizations
from handlers.participant import subscribe_to_newsletter

async def show_volunteer_chat(message: types.Message):
    await message.answer("Присоединяйтесь к чату волонтёров: [https://t.me/+koIOsJQvaww2YTQ6]")

def register_volunteer_handlers(dp: Dispatcher):
    dp.register_message_handler(show_volunteer_chat, text="Общение с волонтёрами")
    dp.register_message_handler(show_organizations, text="Информация про эко-организации")
    dp.register_message_handler(show_events, text="Календарь мероприятий")
    dp.register_message_handler(subscribe_to_newsletter, text="Подписаться на рассылку")
