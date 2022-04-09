from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from view import buttons

cancel_reply = InlineKeyboardMarkup()
cancel_reply.add(InlineKeyboardButton(buttons.cancel_reply, callback_data="cancel_reply"))
