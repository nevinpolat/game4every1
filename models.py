# models.py

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(100), nullable=False, unique=True)
    gender = Column(String(20), nullable=False)
    age = Column(Integer, nullable=False)
    registration_time = Column(DateTime, default=datetime.utcnow)

    # Relationships
    feedbacks = relationship("Feedback", back_populates="user", cascade="all, delete-orphan")
    chat_histories = relationship("ChatHistory", back_populates="user", cascade="all, delete-orphan")

class Feedback(Base):
    __tablename__ = 'feedback'

    feedback_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    feedback_type = Column(String(10), nullable=False)  # e.g., 'up', 'down', 'neutral'
    feedback_time = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="feedbacks")
    chat_histories = relationship("ChatHistory", back_populates="feedback", cascade="all, delete-orphan")

class SearchedGame(Base):
    __tablename__ = 'searched_games'

    game_id = Column(Integer, primary_key=True)
    game_name = Column(String(100), nullable=False)
    subcategory = Column(String(100))
    level = Column(String(100))
    category = Column(String(100))
    searched_time = Column(DateTime, default=datetime.utcnow)

    # Relationships
    chat_histories = relationship("ChatHistory", back_populates="searched_game", cascade="all, delete-orphan")

class ChatHistory(Base):
    __tablename__ = 'chat_history'

    chat_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    game_id = Column(Integer, ForeignKey('searched_games.game_id', ondelete='CASCADE'))
    feedback_id = Column(Integer, ForeignKey('feedback.feedback_id', ondelete='CASCADE'))
    is_related = Column(Boolean, default=False, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="chat_histories")
    feedback = relationship("Feedback", back_populates="chat_histories")
    searched_game = relationship("SearchedGame", back_populates="chat_histories")




