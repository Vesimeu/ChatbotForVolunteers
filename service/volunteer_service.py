from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database import get_db
from models import Volunteer, User

async def subscribe_volunteer_to_event(user_id: int, event_id: int):
    """
    Записывает волонтера на мероприятие.
    Возвращает True в случае успеха, False если уже записан.
    """
    if await is_volunteer_subscribed(user_id, event_id):
        return False  # Уже подписан

    async for session in get_db():
        new_subscription = Volunteer(user_id=user_id, event_id=event_id)
        session.add(new_subscription)
        await session.commit()
        return True

async def get_volunteers_for_event(event_id: int):
    """
    Возвращает список пользователей-волонтеров для конкретного мероприятия.
    """
    async for session in get_db():
        result = await session.execute(
            select(Volunteer)
            .where(Volunteer.event_id == event_id)
            .options(selectinload(Volunteer.user))
        )
        subscriptions = result.scalars().all()
        # Извлекаем пользователей из подписок
        return [sub.user for sub in subscriptions]

async def is_volunteer_subscribed(user_id: int, event_id: int) -> bool:
    """
    Проверяет, записан ли уже волонтер на данное мероприятие.
    """
    async for session in get_db():
        result = await session.execute(
            select(Volunteer).where(
                Volunteer.user_id == user_id,
                Volunteer.event_id == event_id
            )
        )
        return result.scalars().first() is not None 