from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ParseMode

from database import get_db
from service.user_service import get_user_by_telegram_id
from states import RegistrationState
from handlers.utils import role_keyboard


async def delete_user(message: types.Message):
    """
    Удаляет пользователя из базы данных.
    """
    telegram_id = message.from_user.id
    user = await get_user_by_telegram_id(telegram_id)

    if user:
        async for db in get_db():
            async with db as session:
                await session.delete(user)
                await session.commit()
                await message.answer(f"Пользователь {message.from_user.username} был удален из базы данных.")
    else:
        await message.answer("Пользователь не найден.")


async def change_role(message: types.Message):
    """
    Позволяет пользователю сменить свою роль, инициируя процесс выбора роли.
    """
    await message.answer("Пожалуйста, выберите вашу новую роль:", reply_markup=role_keyboard)
    await RegistrationState.waiting_for_role.set()


def register_user_management_handlers(dp: Dispatcher):
    """
    Регистрация обработчиков для команд сброса роли и удаления пользователя.
    """
    dp.register_message_handler(delete_user, commands=["rolereset"], state="*")
    dp.register_message_handler(change_role, commands=["changerole"], state="*")
