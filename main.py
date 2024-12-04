import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.redis import RedisStorage
from utils.config import REDIS_HOST, REDIS_PORT, PROXY_CONFIG
# from handlers.user.start import register_handlers_user
from loader import dp,bot

logging.basicConfig(level=logging.INFO)

async def main():
    # Configure Redis storage
    storage = RedisStorage.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}")

    # Configure Bot with Proxy
    # session = AiohttpSession(**PROXY_CONFIG) if PROXY_CONFIG["proxy"] else None
    # bot = Bot(token=BOT_TOKEN, session=session)

    # Create Dispatcher
    # dp = Dispatcher(storage=storage)

    try:
        logging.info("Бот запущен!")
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Ошибка при запуске бота: {e}")
    finally:
        await bot.session.close()
        await storage.close()

if __name__ == "__main__":
    asyncio.run(main())
