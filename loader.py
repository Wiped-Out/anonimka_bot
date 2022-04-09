import logging

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from aiogram.dispatcher import Dispatcher

import config

bot = Bot(token=config.TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MongoStorage(db_name="anonimka_bot"))

logging.basicConfig(filename="log.log", level=logging.INFO)
log = logging.getLogger("bot")
