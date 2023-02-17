import logging, os

from aiogram import Bot, Dispatcher, executor, types
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.types.web_app_info import WebAppInfo
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup
from aiogram.types.reply_keyboard import KeyboardButton

from dotenv import load_dotenv


load_dotenv(".env")
storage = MemoryStorage()

logging.basicConfig(level=logging.INFO)
bot = Bot(token=os.getenv("TG_TOKEN"))
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=["start"])
async def welcome(message: types.Message):
    if message.from_user.id != message.chat.id:
        return
    await message.reply("It's work")


@dp.message_handler(commands=["map"])
async def welcome(message: types.Message):
    if message.from_user.id != message.chat.id:
        return
    with open("./src/assets/map.jpg", 'rb') as file:
         await bot.send_photo(message.from_user.id, file)


def run() -> None:
    executor.start_polling(dp, skip_updates=False)
