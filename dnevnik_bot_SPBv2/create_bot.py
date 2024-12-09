from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from config import REDIS_URL, TOKEN

storage = RedisStorage.from_url(REDIS_URL)

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(storage=storage)
