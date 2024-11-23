from sqlalchemy import Column, Integer, String,Boolean, ForeignKey, Text, Enum, DateTime, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import Enum
from .database import Base

class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    user_quests = relationship("UserQuest", back_populates="user")

class QuestionSet(Base):
    __tablename__ = "questionset"

    set_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)

    questions = relationship("Question", back_populates="question_set")

class Question(Base):
    __tablename__ = "question"

    question_id = Column(Integer, primary_key=True, index=True)
    set_id = Column(Integer, ForeignKey("questionset.set_id"), nullable=False)
    question_text = Column(Text, nullable=False)

    question_set = relationship("QuestionSet", back_populates="questions")

    answers = relationship("Answer", back_populates="question")
    user_quests = relationship("UserQuest", back_populates="question")


class Answer(Base):
    __tablename__ = "answer"

    answer_id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("question.question_id"), nullable=False)
    answer_text = Column(Text, nullable=False)
    is_correct = Column(Integer, default=0) 

    question = relationship("Question", back_populates="answers")

class UserQuest(Base):
    __tablename__ = "user_quest"

    user_quest_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    question_id = Column(Integer, ForeignKey("question.question_id"), nullable=False)
    
    status = Column(Boolean, nullable=False)
    completed_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    user = relationship("User", back_populates="user_quests")
    question = relationship("Question", back_populates="user_quests")

