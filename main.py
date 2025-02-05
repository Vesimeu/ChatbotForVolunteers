import asyncio
import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from ChatbotForVolunteers.handlers.deleteuser import register_user_management_handlers
from ChatbotForVolunteers.handlers.organizations import register_organization_handlers
from config import BOT_TOKEN
from database import init_db
from handlers.events import register_events_handlers
from ChatbotForVolunteers.handlers.start import register_start_handlers
from ChatbotForVolunteers.handlers.participant import register_participant_handlers, send_event_notifications
from ChatbotForVolunteers.handlers.volunteer import register_volunteer_handlers
from ChatbotForVolunteers.handlers.organizer import register_organizer_handlers
from ChatbotForVolunteers.handlers.feedback import register_feedback_handlers

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Регистрация обработчиков
register_events_handlers(dp)
register_volunteer_handlers(dp)
register_start_handlers(dp)
register_participant_handlers(dp,bot)
register_organizer_handlers(dp)
register_feedback_handlers(dp)
register_organization_handlers(dp)
register_user_management_handlers(dp)
async def on_startup(_):
    """
    Функция, которая выполняется при запуске бота.
    """
    await init_db()  # Инициализация базы данных
    logging.info("Бот запущен и база данных инициализирована.")
    asyncio.create_task(send_event_notifications(bot))

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)