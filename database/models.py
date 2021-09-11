from sqlalchemy import Column, Integer

from database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    telegram_id = Column(Integer, nullable=False)
    reply_message_id = Column(Integer)
