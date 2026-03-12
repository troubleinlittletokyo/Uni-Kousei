from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    tg_id = Column(BigInteger, primary_key=True)
    username = Column(String, nullable=True)

    role = Column(String, default="Student")

    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    subgroup = Column(Integer, default=1)
    faculty = Column(String, nullable=True)
    course = Column(Integer, nullable=True)

    notify_time = Column(Integer, default=10)
    notifications_enable = Column(Boolean, default=True)

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    last_upd = Column(DateTime, default=datetime.utcnow)
    
    lessons = relationship("Lesson", back_populates="group", cascade="all, delete")

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"))

    subject = Column(String, nullable=False)
    teacher = Column(String, nullable=True)
    room = Column(String, nullable=True)

    day_of_week = Column(Integer)
    start_time = Column(String)
    parity = Column(Integer)
    subgroup = Column(Integer, default=0)

    group = relationship("Group", back_populates="lessons")