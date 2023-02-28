from dataclasses import dataclass

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.store.database.sqlalchemy_base import db


@dataclass
class Theme:
    id: int | None
    title: str


@dataclass
class Question:
    id: int | None
    title: str
    theme_id: int
    answers: list["Answer"]


@dataclass
class Answer:
    title: str
    is_correct: bool


class ThemeModel(db):
    __tablename__ = "themes"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, unique=True)


class QuestionModel(db):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, unique=True)
    theme_id = Column(ForeignKey("themes.id", ondelete="CASCADE"), nullable=False)
    # theme = relationship("ThemeModel", back_populates="question")
    answers = relationship(
        "AnswerModel", back_populates="question", cascade="all, delete"
    )


class AnswerModel(db):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    question_id = Column(ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    question = relationship("QuestionModel", back_populates="answers")
