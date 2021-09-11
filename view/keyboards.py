from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton

import view.buttons as buttons

back_to_main_menu_kb = ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
back_to_main_menu_kb.add(KeyboardButton(buttons.back_to_main_menu))

remove_kb = ReplyKeyboardRemove()

cancel_reply = InlineKeyboardMarkup()
cancel_reply.add(InlineKeyboardButton(buttons.cancel_reply, callback_data="cancel_reply"))
