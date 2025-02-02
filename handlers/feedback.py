from aiogram import types
from aiogram.dispatcher import Dispatcher
from ChatbotForVolunteers.database import get_db
from ChatbotForVolunteers.models import Feedback

async def send_feedback(message: types.Message):
    """
    Обработчик для отправки отзыва.
    """
    async for db in get_db():  # Используем `async for` вместо `await`
        async with db as session:
            feedback = Feedback(
                user_id=message.from_user.id,
                message=message.text,
            )
            session.add(feedback)
            await session.commit()
            await message.answer("Спасибо за ваш отзыв!")

def register_feedback_handlers(dp: Dispatcher):
    """
    Регистрация обработчиков для отзывов.
    """
    dp.register_message_handler(send_feedback, commands=["feedback"])