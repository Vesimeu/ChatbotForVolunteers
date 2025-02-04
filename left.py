from ChatbotForVolunteers.models import Base
from ChatbotForVolunteers.database import engine

Base.metadata.drop_all(engine)  # Удаляет старые таблицы
Base.metadata.create_all(engine)  # Создаёт новые таблицы
