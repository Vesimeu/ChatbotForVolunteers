from aiogram import types
from aiogram.dispatcher import Dispatcher

async def show_volunteer_chat(message: types.Message):
    await message.answer("Присоединяйтесь к чату волонтёров: [ссылка на чат]")

def register_volunteer_handlers(dp: Dispatcher):
    dp.register_message_handler(show_volunteer_chat, text="Общение с волонтёрами")
