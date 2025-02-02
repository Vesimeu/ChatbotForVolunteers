from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from ChatbotForVolunteers.states import RegistrationState
from ChatbotForVolunteers.service.user_service import get_user_by_telegram_id, create_user, update_user_role

# Клавиатуры для разных ролей
participant_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("Просмотреть мероприятия"),
    KeyboardButton("Подписаться на рассылку")
)

volunteer_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("Мои задачи"),
    KeyboardButton("Подписаться на рассылку")
)

organizer_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("Создать мероприятие"),
    KeyboardButton("Управление мероприятиями")
)

role_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("Участник"),
    KeyboardButton("Волонтёр"),
    KeyboardButton("Организатор"),
    KeyboardButton("Оставить отзыв")
)


async def start_command(message: types.Message):
    """
    Обработчик команды /start.
    """
    user = await get_user_by_telegram_id(message.from_user.id)

    if not user:
        await create_user(message.from_user.id, message.from_user.username)
        await message.answer("Добро пожаловать! Выберите вашу роль:", reply_markup=role_keyboard)
        await RegistrationState.waiting_for_role.set()  # Запускаем FSM
    else:
        # Если пользователь уже выбран, показываем соответствующую клавиатуру
        if user.role == "participant":
            await message.answer("С возвращением, участник! Чем могу помочь?", reply_markup=participant_keyboard)
        elif user.role == "volunteer":
            await message.answer("С возвращением, волонтёр! Чем могу помочь?", reply_markup=volunteer_keyboard)
        elif user.role == "organizer":
            await message.answer("С возвращением, организатор! Чем могу помочь?", reply_markup=organizer_keyboard)
        else:
            await message.answer("С возвращением! Чем могу помочь?", reply_markup=role_keyboard)


async def process_role_selection(message: types.Message, state: FSMContext):
    """
    Обрабатывает выбор роли.
    """
    role_mapping = {
        "Участник": "participant",
        "Волонтёр": "volunteer",
        "Организатор": "organizer"
    }

    if message.text in role_mapping:
        role = role_mapping[message.text]
        await update_user_role(message.from_user.id, role)

        # Отправляем клавиатуру в зависимости от выбранной роли
        if role == "participant":
            await message.answer(f"Вы выбрали роль: {message.text}. Теперь можете пользоваться ботом!",
                                 reply_markup=participant_keyboard)
        elif role == "volunteer":
            await message.answer(f"Вы выбрали роль: {message.text}. Теперь можете пользоваться ботом!",
                                 reply_markup=volunteer_keyboard)
        elif role == "organizer":
            await message.answer(f"Вы выбрали роль: {message.text}. Теперь можете пользоваться ботом!",
                                 reply_markup=organizer_keyboard)

        await state.finish()  # Завершаем состояние
    else:
        await message.answer("Пожалуйста, выберите роль из предложенных вариантов.")


def register_role_handler(dp: Dispatcher):
    dp.register_message_handler(process_role_selection, state=RegistrationState.waiting_for_role)


def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=["start"])
