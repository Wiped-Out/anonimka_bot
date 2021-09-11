from aiogram.dispatcher.filters.state import StatesGroup, State


class User(StatesGroup):
    MAIN_MENU = State()
    REPLY_TO_MESSAGE = State()
