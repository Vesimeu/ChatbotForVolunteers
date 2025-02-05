from sqlalchemy.future import select
from database import get_db
from models import Feedback

async def save_feedback(user_id: int, message: str):
    """
    Сохраняет отзыв в базе данных.
    """
    async for db in get_db():
        async with db as session:
            feedback = Feedback(user_id=user_id, message=message)
            session.add(feedback)
            await session.commit()
