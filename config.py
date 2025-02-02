import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Токен бота
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Настройки базы данных
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./volunteer_bot.db")