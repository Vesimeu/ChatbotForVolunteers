from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=True)
    role = Column(String, default='participant')  # participant, volunteer, organizer, admin
    subscribed = Column(Boolean, default=False)  # Подписан ли на рассылку

    # Связи
    events_organized = relationship('Event', back_populates='organizer')  # ✅ Исправлено
    feedbacks = relationship('Feedback', back_populates='user')
    volunteer_events = relationship('Volunteer', back_populates='user')

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    description = Column(String, nullable=False)
    location = Column(String, nullable=False)
    contact_info = Column(String, nullable=False)
    volunteers_needed = Column(Integer, nullable=False)
    organizer_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Связи
    organizer = relationship('User', back_populates='events_organized')  # ✅ Исправлено
    volunteers = relationship('Volunteer', back_populates='event')

class Volunteer(Base):
    __tablename__ = 'volunteers'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)

    # Связи
    user = relationship('User', back_populates='volunteer_events')
    event = relationship('Event', back_populates='volunteers')

class Feedback(Base):
    __tablename__ = 'feedbacks'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    message = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    # Связи
    user = relationship('User', back_populates='feedbacks')

class Organization(Base):
    __tablename__ = 'organizations'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    contact_info = Column(String, nullable=False)
    website = Column(String, nullable=True)