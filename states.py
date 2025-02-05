from aiogram.dispatcher.filters.state import State, StatesGroup

class RegistrationState(StatesGroup):
    waiting_for_password = State()
    waiting_for_role = State()  # Ожидание выбора роли
    waiting_for_feedback = State()  # Ожидание отзыва
