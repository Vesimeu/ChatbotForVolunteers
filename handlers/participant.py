import asyncio
from datetime import datetime, timedelta

import pytz
from aiogram import types, Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils.exceptions import ChatNotFound
from sqlalchemy.testing.plugin.plugin_base import logging
import logging
from ChatbotForVolunteers.database import get_db
from ChatbotForVolunteers.handlers.events import show_events
from ChatbotForVolunteers.handlers.organizations import show_organizations
from ChatbotForVolunteers.service.event_service import get_all_events,get_all_events_with_session
from ChatbotForVolunteers.service.user_service import update_subscription_status, get_subscribed_users, get_subscribed_users_with_session

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
bot: Bot  # 👈 Бот должен быть передан в этом файле
# Часовой пояс Екатеринбурга (UTC+5)
ekaterinburg_tz = pytz.timezone('Asia/Yekaterinburg')
async def subscribe_to_newsletter(message: types.Message):
    """
    Подписывает пользователя на рассылку уведомлений о мероприятиях за 2 дня.
    """
    success = await update_subscription_status(message.from_user.id, True)
    if success:
        await message.answer("✅ Вы подписались на рассылку!")
    else:
        await message.answer("⚠ Сначала зарегистрируйтесь через /start.")

async def send_event_notifications(bot: Bot):
    """
    Фоновая задача, которая проверяет мероприятия и отправляет уведомления подписанным пользователям.
    """
    while True:
        async for db in get_db():
            async with db as session:
                events = await get_all_events_with_session(session)
                subscribers = await get_subscribed_users_with_session(session)

                # Получаем текущее время в Екатеринбурге
                now = datetime.now(ekaterinburg_tz)

                # Преобразуем event.date в осведомленную дату, если она наивная
                upcoming_events = [
                    event for event in events
                    if timedelta(days=2) >= event.date.astimezone(ekaterinburg_tz) - now > timedelta(0)
                ]

                logging.info(f"Текущее время в Екатеринбурге: {now}")

                for event in upcoming_events:
                    message_text = (
                        f"📢 Напоминание!\n"
                        f"📅 **Скоро мероприятие:** {event.name}\n"
                        f"📆 Дата: {event.date.strftime('%Y-%m-%d %H:%M')}\n"
                        f"📍 Место: {event.location}\n"
                        f"🔗 Контакты: {event.contact_info}\n\n"
                        f"⏳ Осталось менее 2 дней!"
                    )

                    for user in subscribers:
                        try:
                            await bot.send_message(user.telegram_id, message_text)
                        except ChatNotFound:
                            logging.info(f"⚠ Пользователь {user.telegram_id} не найден, удаляем из подписки.")
                            await update_subscription_status(user.telegram_id, False)

        await asyncio.sleep(3600)  # 📌 Проверяем каждую минуту

def register_participant_handlers(dp: Dispatcher, bot_instance: Bot):
    global bot
    bot = bot_instance
    dp.register_message_handler(show_organizations, text="Информация про эко-организации")
    dp.register_message_handler(show_events, text="Календарь мероприятий")
    dp.register_message_handler(subscribe_to_newsletter, text="Подписаться на рассылку")