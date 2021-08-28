from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.bot.api import TelegramAPIServer

from data import config

# local_server = TelegramAPIServer.from_base('http://localhost:8081')
local_server = TelegramAPIServer.from_base('https://api.telegram.org')

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML, server=local_server)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
