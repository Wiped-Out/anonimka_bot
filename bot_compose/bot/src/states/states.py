from aiogram.dispatcher.filters.state import State, StatesGroup


class User(StatesGroup):
    REPLY_TO_MESSAGE = State()
