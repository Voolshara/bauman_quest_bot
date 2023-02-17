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

from typing import Optional

from dotenv import load_dotenv


load_dotenv(".env")
storage = MemoryStorage()


class CSV_worker:
    def __init__(self):
        self.events_csv = "./src/events.csv"
        self.commands_csv = "./src/commands.csv"

    def add_line(self, filename: str, add_s: str) -> None:
        with open(filename, 'a', encoding='utf-8') as file:
            file.write(add_s)

    def change_line(self, file_name: str, search_id: int, template: str, new_val_id: int, new_val: str) -> None:
        with open(file_name, 'r', encoding='utf-8') as file:
            all_lines = file.readlines() 

        with open(file_name, 'w', encoding='utf-8') as file:
            out_s = [all_lines[0].strip()]
            for line in all_lines[1:]:
                line_split = line.split(', ')
                if line_split[search_id] == template:
                    line_split[new_val_id] = new_val
                    out_s.append(", ".join(line_split))
                else:
                    out_s.append(line.strip())
            file.write("\n".join(out_s))

    def get_elem(self, file_name: str, search_id: int, template: str, out_id: str) -> Optional[str]:
        with open(file_name, 'r', encoding='utf-8') as file:
            for line in file.readlines():
                line_split = line.split(', ')
                if line_split[search_id] == template:
                    return line_split[out_id] 
        return None

    def get_all(self, file_name: str, search_id: int, template: str) -> list:
        out_id = []
        with open(file_name, 'r', encoding='utf-8') as file:
            file.readline()
            if template == '*':
                for line in file.readlines():
                    line_split = line.split(', ')
                    out_id.append(line_split) 
            else:
                for line in file.readlines():
                    line_split = line.split(', ')
                    if line_split[search_id].strip() == template:
                        out_id.append(line_split) 
        return out_id
    

logging.basicConfig(level=logging.INFO)
bot = Bot(token=os.getenv("TG_TOKEN"))
dp = Dispatcher(bot, storage=storage)
db = CSV_worker()
    

@dp.message_handler(commands=["start"])
async def welcome(message: types.Message):
    if message.from_user.id != message.chat.id:
        return
    await message.reply("/get_events\n")
    if db.get_elem(db.commands_csv, 0, str(message.from_user.id), 0) is None:
        db.add_line(db.commands_csv, ", ".join([str(message.from_user.id), "null", ""]) + '\n')
    



@dp.message_handler(commands=["map"])
async def map(message: types.Message):
    if message.from_user.id != message.chat.id:
        return
    with open("./src/assets/map.jpg", 'rb') as file:
        await bot.send_photo(message.from_user.id, file)

@dp.message_handler(commands=["get_events"])
async def get_events(message: types.Message):
    if message.from_user.id != message.chat.id:
        return
    events_list = db.get_all(db.events_csv, 2, "1")
    if len(events_list) == 0:
        await message.reply("Свободных точек пока нет (")
        return
    await message.reply("Свободные точки:\n%s" % "\n".join([x[1] for x in events_list]))

@dp.message_handler(commands=["odin"])
async def map(message: types.Message):
    code_ = "/odin"
    if message.from_user.id != message.chat.id:
        return
    
    if db.get_elem(db.commands_csv, 0, str(message.from_user.id), 1) != "null":
        await message.reply("Сначала заверши прошлую точку")
        return

    check_is_free = db.get_elem(db.events_csv, 1, code_, 2)
    if check_is_free is None:
        await message.reply('Непредвиденная ошибка\nОбратись @Sta_tun_slav')
        return
    if check_is_free == "0":
        await message.reply("Извини, эта точка уже занята\nВыбери другую /get_events")
        return
    db.change_line(db.events_csv, 1, code_, 2, "0")
    db.change_line(db.commands_csv, 0, str(message.from_user.id), 1, code_)
    await message.reply("Точка %s выбрана" % code_)


@dp.message_handler(commands=["dva"])
async def map(message: types.Message):
    code_ = "/dva"
    if message.from_user.id != message.chat.id:
        return
    
    if db.get_elem(db.commands_csv, 0, str(message.from_user.id), 1) != "null":
        await message.reply("Сначала заверши прошлую точку")
        return

    check_is_free = db.get_elem(db.events_csv, 1, code_, 2)
    if check_is_free is None:
        await message.reply('Непредвиденная ошибка\nОбратись @Sta_tun_slav')
        return
    if check_is_free == "0":
        await message.reply("Извини, эта точка уже занята\nВыбери другую /get_events")
        return
    db.change_line(db.events_csv, 1, code_, 2, "0")
    db.change_line(db.commands_csv, 0, str(message.from_user.id), 1, code_)
    await message.reply("Точка %s выбрана" % code_)


@dp.message_handler(commands=["three"])
async def map(message: types.Message):
    code_ = "/three"
    if message.from_user.id != message.chat.id:
        return
    
    if db.get_elem(db.commands_csv, 0, str(message.from_user.id), 1) != "null":
        await message.reply("Сначала заверши прошлую точку")
        return

    check_is_free = db.get_elem(db.events_csv, 1, code_, 2)
    if check_is_free is None:
        await message.reply('Непредвиденная ошибка\nОбратись @Sta_tun_slav')
        return
    if check_is_free == "0":
        await message.reply("Извини, эта точка уже занята\nВыбери другую /get_events")
        return
    db.change_line(db.events_csv, 1, code_, 2, "0")
    db.change_line(db.commands_csv, 0, str(message.from_user.id), 1, code_)
    await message.reply("Точка %s выбрана" % code_)

def run() -> None:
    executor.start_polling(dp, skip_updates=False)
