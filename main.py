from aiogram import Bot, Dispatcher, executor
from dotenv import load_dotenv
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from voxel_scripts import database

import os

load_dotenv()
bot = Bot(os.getenv('TOKEN'))
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

async def on_startup(_):
    await database.db_start()
    print("Бот запущен")


if __name__ == '__main__':
    from voxel_scripts import handlers
    executor.start_polling(handlers.dp, on_startup=on_startup, skip_updates=True)
