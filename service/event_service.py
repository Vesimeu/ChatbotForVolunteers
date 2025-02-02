from sqlalchemy.future import select
from ChatbotForVolunteers.database import get_db
from ChatbotForVolunteers.models import Event

async def get_all_events():
    """
    Получает список всех мероприятий.
    """
    async for db in get_db():
        async with db as session:
            result = await session.execute(select(Event))
            return result.scalars().all()

async def get_event_by_id(event_id: int):
    """
    Получает мероприятие по ID.
    """
    async for db in get_db():
        async with db as session:
            result = await session.execute(select(Event).where(Event.id == event_id))
            return result.scalars().first()

async def create_event(name: str, date, description: str, location: str, contact_info: str, volunteers_needed: int, organizer_id: int):
    """
    Создаёт новое мероприятие.
    """
    async for db in get_db():
        async with db as session:
            event = Event(
                name=name,
                date=date,
                description=description,
                location=location,
                contact_info=contact_info,
                volunteers_needed=volunteers_needed,
                organizer_id=organizer_id
            )
            session.add(event)
            await session.commit()
            return event

async def delete_event(event_id: int):
    """
    Удаляет мероприятие по ID.
    """
    async for db in get_db():
        async with db as session:
            result = await session.execute(select(Event).where(Event.id == event_id))
            event = result.scalars().first()
            if event:
                await session.delete(event)
                await session.commit()
                return True
            return False

async def update_event(event_id: int, **kwargs):
    """
    Обновляет информацию о мероприятии. Передавать можно любые аргументы, например:
    update_event(event_id=1, name="Новое название", description="Новое описание")
    """
    async for db in get_db():
        async with db as session:
            result = await session.execute(select(Event).where(Event.id == event_id))
            event = result.scalars().first()
            if event:
                for key, value in kwargs.items():
                    if hasattr(event, key):
                        setattr(event, key, value)
                await session.commit()
                return event
            return None
