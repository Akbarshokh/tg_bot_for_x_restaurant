# from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.client.default import DefaultBotProperties
# from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession

from utils.config import BOT_TOKEN, PROXY_CONFIG
session = AiohttpSession(**PROXY_CONFIG) if PROXY_CONFIG["proxy"] else None
bot = Bot(token=BOT_TOKEN, session=session)

# bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()