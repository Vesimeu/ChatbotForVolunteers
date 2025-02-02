from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import Base
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Получение пути к базе данных из переменной окружения
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./volunteer_bot.db")

# Создание асинхронного движка для работы с базой данных
engine = create_async_engine(DATABASE_URL, echo=True)

# Создание асинхронной фабрики сессий
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def init_db():
    """
    Инициализация базы данных: создание всех таблиц.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    """
    Асинхронный генератор сессий базы данных.
    """
    async with AsyncSessionLocal() as session:
        yield session  # Передача сессии через `yield`
