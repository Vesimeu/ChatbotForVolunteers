from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from ChatbotForVolunteers.states import RegistrationState
from ChatbotForVolunteers.service.user_service import get_user_by_telegram_id, create_user, update_user_role

# Клавиатура выбора роли
role_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("Участник"),
    KeyboardButton("Волонтёр"),
    KeyboardButton("Организатор")
)

async def start_command(message: types.Message):
    """
    Обработчик команды /start.
    """
    user = await get_user_by_telegram_id(message.from_user.id)

    if not user:
        await create_user(message.from_user.id, message.from_user.username)
        await message.answer("Добро пожаловать! Выберите вашу роль:", reply_markup=role_keyboard)
        await RegistrationState.waiting_for_role.set()
    else:
        from ChatbotForVolunteers.handlers.utils import get_keyboard_for_role
        keyboard = get_keyboard_for_role(user.role)
        await message.answer("С возвращением! Чем могу помочь?", reply_markup=keyboard)

async def process_role_selection(message: types.Message, state: FSMContext):
    """
    Обрабатывает выбор и смену роли.
    """
    role_mapping = {
        "Участник": "participant",
        "Волонтёр": "volunteer",
        "Организатор": "organizer"
    }

    if message.text in role_mapping:
        role = role_mapping[message.text]
        await update_user_role(message.from_user.id, role)

        from ChatbotForVolunteers.handlers.utils import get_keyboard_for_role
        keyboard = get_keyboard_for_role(role)

        await message.answer(f"Вы выбрали роль: {message.text}.", reply_markup=keyboard)
        await state.finish()
    else:
        await message.answer("Пожалуйста, выберите роль из предложенных вариантов.")

def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=["start"])
    dp.register_message_handler(process_role_selection, state=RegistrationState.waiting_for_role)
