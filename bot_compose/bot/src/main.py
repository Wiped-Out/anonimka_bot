from aiogram.utils import executor
from core.config import logger
from handlers import dp
from loader import dp  # noqa: F811, WPS440


async def on_startup(dispatcher):
    logger.info('Bot started')


async def on_shutdown(dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
