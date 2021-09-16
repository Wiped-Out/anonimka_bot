import aiogram.utils.exceptions
from aiogram import types

from loader import bot, dp
from sqlalchemy.exc import IntegrityError
from database import crud
from utils import utils
from states import states
import config
from view import messages, keyboards
from typing import Union


@dp.message_handler(commands=["start"], state="*")
async def start(message: types.Message):
    try:
        crud.create_user(telegram_id=message.from_user.id)
        await states.User.MAIN_MENU.set()
        await message.answer(text=messages.MAIN_MENU, reply_markup=keyboards.remove_kb)
    except IntegrityError:
        await states.User.MAIN_MENU.set()
        await message.answer(text=messages.MAIN_MENU, reply_markup=keyboards.remove_kb)
    except Exception as error:
        await utils.error_except(message.from_user.id, error)


@dp.message_handler(state=states.User.REPLY_TO_MESSAGE, content_types=[types.ContentType.ANY])
async def reply_to_message(message: types.Message):
    """
    Пользователь отвечает на сообщение

    :param message: Объект сообщения Telegram
    """

    reply_to_message_id = crud.get_user(user_id=message.from_user.id).reply_message_id
    crud.edit_reply_message_id(telegram_id=message.from_user.id, message_id_to_reply=None)

    await send_message_to_channel(message=message, reply_to_message_id=reply_to_message_id)


@dp.message_handler(state="*", content_types=[types.ContentType.ANY])
async def all_messages(message: types.Message):
    # Проверяем, пересылаемое ли сообщение
    if not (message.forward_from or message.forward_from_chat):
        await send_message_to_channel(message=message)
        return

    if message.forward_from_chat:
        # Если пересылают из анонимки, то это реплай на одно из сообщений
        if message.forward_from_chat.id == config.CHANNEL_ID:
            await switch_to_sending_reply(message)
            return

    # Если сообщение было переслано не из анонимки, то это не реплай.
    # Пересылаем сообщение в анонимку
    await bot.forward_message(
        chat_id=config.CHANNEL_ID, from_chat_id=message.from_user.id,
        message_id=message.message_id)

    await bot.send_message(chat_id=message.from_user.id, text=messages.FORWARDED_SUCCESSFUL)


@dp.callback_query_handler(text_contains="cancel_reply", state=states.User.REPLY_TO_MESSAGE)
async def cancel_reply(query: types.CallbackQuery):
    try:
        await bot.edit_message_reply_markup(
            reply_markup=None, chat_id=query.from_user.id,
            message_id=query.message.message_id)
    except aiogram.utils.exceptions.MessageCantBeEdited:
        pass

    await states.User.MAIN_MENU.set()
    await bot.send_message(chat_id=query.from_user.id, text=messages.MAIN_MENU, reply_markup=keyboards.remove_kb)


async def switch_to_sending_reply(message: types.Message):
    await states.User.REPLY_TO_MESSAGE.set()
    crud.edit_reply_message_id(
        telegram_id=message.from_user.id,
        message_id_to_reply=message.forward_from_message_id)

    await message.answer(text=messages.SEND_REPLY, reply_markup=keyboards.cancel_reply)


async def send_message_to_channel(message: types.Message, reply_to_message_id: Union[int, None] = None):
    """
    Отправляет сообщение в анонимку

    :param message: Объект сообщения от Telegram
    :param reply_to_message_id: ID сообщения в анонимке, на которое отвечает пользователь
    """

    if message.content_type == "text":
        await bot.send_message(
            chat_id=config.CHANNEL_ID, text=message.text,
            reply_to_message_id=reply_to_message_id)

    elif message.content_type == "photo":
        await bot.send_photo(
            chat_id=config.CHANNEL_ID, photo=message.photo[0].file_id,
            caption=message.caption, reply_to_message_id=reply_to_message_id)

    elif message.content_type == "audio":
        await bot.send_audio(
            chat_id=config.CHANNEL_ID, audio=message.audio.file_id,
            caption=message.caption, reply_to_message_id=reply_to_message_id)

    elif message.content_type == "video":
        await bot.send_video(
            chat_id=config.CHANNEL_ID, video=message.video.file_id,
            caption=message.caption, reply_to_message_id=reply_to_message_id)

    elif message.content_type == "sticker":
        await bot.send_sticker(
            chat_id=config.CHANNEL_ID, sticker=message.sticker.file_id,
            reply_to_message_id=reply_to_message_id)

    elif message.content_type == "voice":
        await bot.send_voice(
            chat_id=config.CHANNEL_ID, voice=message.voice.file_id,
            reply_to_message_id=reply_to_message_id)

    elif message.content_type == "poll":
        await bot.send_poll(
            chat_id=config.CHANNEL_ID, question=message.poll.question,
            options=[option.text for option in message.poll.options], is_anonymous=True,
            allows_multiple_answers=message.poll.allows_multiple_answers
        )

    elif message.content_type == "animation":
        await bot.send_animation(
            chat_id=config.CHANNEL_ID, animation=message.animation.file_id
        )

    await message.answer(text=messages.POST_SENT, reply_markup=keyboards.remove_kb)
    await states.User.MAIN_MENU.set()
