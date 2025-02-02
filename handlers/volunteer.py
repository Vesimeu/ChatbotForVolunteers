from aiogram import types
from aiogram.dispatcher import Dispatcher
from ChatbotForVolunteers.service.user_service import update_subscription_status

async def subscribe_to_newsletter(message: types.Message):
    """
    Обработчик для подписки на рассылку.
    """
    success = await update_subscription_status(message.from_user.id, True)

    if success:
        await message.answer("Вы подписались на рассылку!")
    else:
        await message.answer("Сначала зарегистрируйтесь с помощью команды /start.")

def register_volunteer_handlers(dp: Dispatcher):
    dp.register_message_handler(subscribe_to_newsletter, commands=["subscribe"])
