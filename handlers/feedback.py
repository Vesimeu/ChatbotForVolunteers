from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from database import get_db
from models import Feedback

class FeedbackState(StatesGroup):
    waiting_for_text = State()

async def start_feedback(message: types.Message):
    """
    Запускает процесс отправки отзыва.
    """
    await message.answer("Напишите ваш отзыв и отправьте его.")
    await FeedbackState.waiting_for_text.set()

async def save_feedback(message: types.Message, state: FSMContext):
    """
    Сохраняет отзыв в базе данных.
    """
    async for db in get_db():
        async with db as session:
            feedback = Feedback(
                user_id=message.from_user.id,
                message=message.text,
            )
            session.add(feedback)
            await session.commit()
            await message.answer("Спасибо за ваш отзыв!")
    await state.finish()

def register_feedback_handlers(dp: Dispatcher):
    """
    Регистрация обработчиков для отзывов.
    """
    dp.register_message_handler(start_feedback, text="Оставить отзыв")
    dp.register_message_handler(save_feedback, state=FeedbackState.waiting_for_text)
