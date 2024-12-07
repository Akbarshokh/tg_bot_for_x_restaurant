import logging
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.redis import RedisStorage
from utils.config import BOT_TOKEN, REDIS_HOST, REDIS_PORT, PROXY_CONFIG
from handlers.user import routers_list

session = AiohttpSession(**PROXY_CONFIG) if PROXY_CONFIG["proxy"] else None
bot = Bot(token=BOT_TOKEN, session=session)

storage = RedisStorage.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}")

dp = Dispatcher( storage=storage)

for router in routers_list:
    dp.include_router(router)

logging.basicConfig(
    level=logging.INFO,
    format=u"%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)