import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import BOT_TOKEN
from database import init_db
from handlers.start import register_start_handlers
from handlers.events import register_events_handlers
from handlers.volunteer import register_volunteer_handlers
from handlers.feedback import register_feedback_handlers
from handlers.admin import register_admin_handlers

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Регистрация обработчиков
register_start_handlers(dp)
register_events_handlers(dp)
register_volunteer_handlers(dp)
register_feedback_handlers(dp)
register_admin_handlers(dp)

async def on_startup(_):
    """
    Функция, которая выполняется при запуске бота.
    """
    await init_db()  # Инициализация базы данных
    logging.info("Бот запущен и база данных инициализирована.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)