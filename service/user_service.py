from sqlalchemy.future import select
from database import get_db
from models import User

async def get_user_by_telegram_id(telegram_id: int):
    """
    Получает пользователя по telegram_id.
    """
    async for db in get_db():
        async with db as session:
            result = await session.execute(select(User).where(User.telegram_id == telegram_id))
            return result.scalars().first()

async def create_user(telegram_id: int, username: str = None, role: str = "participant"):
    """
    Создаёт нового пользователя в базе.
    """
    async for db in get_db():
        async with db as session:
            user = User(
                telegram_id=telegram_id,
                username=username,
                role=role,
                subscribed=False
            )
            session.add(user)
            await session.commit()
            return user

async def is_user_subscribed(telegram_id: int) -> bool:
    """
    Проверяет, подписан ли пользователь на рассылку.
    """
    user = await get_user_by_telegram_id(telegram_id)
    return user.subscribed if user else False

async def get_subscribed_users():
    """
    Получает всех пользователей, подписанных на рассылку.
    Возвращает список объектов User с `telegram_id`.
    """
    async for db in get_db():
        async with db as session:
            result = await session.execute(select(User).where(User.is_subscribed == True))
            return result.scalars().all()

async def get_subscribed_users_with_session(session):
    """
    Получает всех пользователей, подписанных на рассылку, с использованием переданной сессии.
    Возвращает список объектов User с `telegram_id`.
    """
    result = await session.execute(select(User).where(User.subscribed == True))
    return result.scalars().all()


async def update_subscription_status(telegram_id: int, status: bool):
    """
    Обновляет статус подписки пользователя.
    """
    async for db in get_db():
        async with db as session:
            result = await session.execute(select(User).where(User.telegram_id == telegram_id))
            user = result.scalars().first()
            if user:
                user.subscribed = status
                await session.commit()
                return True
            return False


async def update_user_role(telegram_id: int, new_role: str) -> bool:
    """
    Обновляет роль пользователя.
    """
    valid_roles = ["participant", "volunteer", "organizer", "admin"]
    if new_role not in valid_roles:
        return False  # Если роль не из допустимых, возвращаем False

    async for db in get_db():
        async with db as session:
            result = await session.execute(select(User).where(User.telegram_id == telegram_id))
            user = result.scalars().first()
            if user:
                user.role = new_role
                await session.commit()
                return True
            return False  # Если пользователь не найден, возвращаем False

