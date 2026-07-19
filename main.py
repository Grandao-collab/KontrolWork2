import asyncio
import logging
import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from db.database import init_db
from src.handlers import router

async def main():
    logging.basicConfig(level=logging.INFO)
    
    # Инициализируем БД при старте
    init_db()
    
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    
    print("Бот успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())