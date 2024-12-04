# from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.client.default import DefaultBotProperties
# from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher

from utils.config import BOT_TOKEN


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()