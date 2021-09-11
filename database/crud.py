from database.database import SessionLocal
from database.models import User
from typing import Union


def create_user(telegram_id: int) -> User:
    """
    Добавляет пользователя в базу данных

    :param telegram_id: Telegram ID пользователя
    """

    session = SessionLocal()
    db_user = User(telegram_id=telegram_id)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user(user_id: int) -> User:
    session = SessionLocal()
    return session.query(User).filter(User.telegram_id == user_id).first()


def edit_reply_message_id(telegram_id: int, message_id_to_reply: Union[int, None]):
    session = SessionLocal()
    user = session.query(User).filter_by(telegram_id=telegram_id)
    user.update({"reply_message_id": message_id_to_reply})
    session.commit()
