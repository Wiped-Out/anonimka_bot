from aiogram import types
from aiogram.dispatcher import FSMContext

import config
from loader import dp
from states import states
from view import messages, keyboards


@dp.message_handler(commands=["start"], state="*")
async def start_command(message: types.Message):
    await message.answer(text=messages.MAIN_MENU, reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=states.User.REPLY_TO_MESSAGE, content_types=types.ContentType.ANY)
async def reply_to_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            reply_to_message_id = data["message_id"]
        except KeyError:
            reply_to_message_id = None

    await state.reset_state(with_data=True)
    await message.send_copy(chat_id=config.CHANNEL_ID, reply_to_message_id=reply_to_message_id)
    await message.answer(messages.POST_SENT)


@dp.message_handler(content_types=types.ContentType.ANY, state="*")
async def messages_handler(message: types.Message, state: FSMContext):
    # Сообщение ниоткуда не пересылали, просто отправляем его в анонимку
    if not (message.forward_from or message.forward_from_chat):
        await message.send_copy(chat_id=config.CHANNEL_ID)
        return await message.answer(messages.POST_SENT)

    # Сообщение переслано из анонимки, значит, это реплай
    if message.forward_from_chat and message.forward_from_chat.id == config.CHANNEL_ID:
        async with state.proxy() as data:
            data["message_id"] = message.forward_from_message_id

        await states.User.REPLY_TO_MESSAGE.set()
        return await message.answer(text=messages.SEND_REPLY, reply_markup=keyboards.cancel_reply)

    # На этом этапе остаются только сообщения, которые пересланы откуда-либо, но не из анонимки
    await message.forward(chat_id=config.CHANNEL_ID)
    await message.answer(text=messages.FORWARDED)


@dp.callback_query_handler(text_contains="cancel_reply", state=states.User.REPLY_TO_MESSAGE)
async def cancel_reply(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_reply_markup(reply_markup=None)

    await state.reset_state(with_data=True)
    await query.message.answer(text=messages.MAIN_MENU, reply_markup=types.ReplyKeyboardRemove())
