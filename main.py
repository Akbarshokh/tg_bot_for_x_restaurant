import asyncio
import logging
from loader import bot, dp

async def main():
    try:
        logging.info("Бот запущен!")
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Ошибка при запуске бота: {e}")
    finally:
        await bot.session.close()
        await dp.storage.close()

if __name__ == "__main__":
    asyncio.run(main())
