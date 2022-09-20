from dotenv import load_dotenv
from loguru import logger
from pydantic import BaseSettings

logger.add(
    'logs.log',
    format='{time} {level} {message}',
    level='DEBUG',
    rotation='10 KB',
    compression='zip',
)

load_dotenv()


class Settings(BaseSettings):
    TOKEN: str
    CHANNEL_ID: int

    REDIS_HOST: str
    REDIS_PORT: int


settings = Settings()
