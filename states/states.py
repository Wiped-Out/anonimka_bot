from aiogram.dispatcher.filters.state import StatesGroup, State


class User(StatesGroup):
    REPLY_TO_MESSAGE = State()
