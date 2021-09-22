import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
import datetime
import uuid
import os
from settings import TOKEN
from sqlite3.dbapi2 import Cursor
from PPTX_GENERATOR import PPTX_GENERATOR 
import sqlite3
API_TOKEN = TOKEN

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons = ["получить сертификат"]
keyboard.add(*buttons)

@dp.message_handler(commands=['start', 'help', 'сертификат'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Привет, "+ message.from_user.first_name + "!\n👋🏼😀\nЯ Квантоша, бот, созданный для отправки сертификата о посещении дня\
		открытых дверей\nНапиши мне своё имя и я отправлю тебе твой сертификат", reply_markup=keyboard)

@dp.message_handler(Text(equals="получить сертификат"))
async def certificate(message: types.Message):
	await message.answer("Напиши мне свои ФИО", reply_markup=keyboard)

@dp.message_handler(regexp='(^cat[s]?$|puss)')
async def cats(message: types.Message):
    with open('data/cats.jpg', 'rb') as photo:
        await message.reply_photo(photo, caption='Cats are here 😺', reply_markup=keyboard)


@dp.message_handler()
async def echo(message: types.Message):
	await message.answer("Твой сертификат создаётся, подожди немного")
	now = str(datetime.date.today().day)
	now += "-" + str(datetime.date.today().month)
	now += "-" + str(datetime.date.today().year)
	UID = uuid.uuid4().hex #уникальный идентификатор
	file = PPTX_GENERATOR(message.text, UID, now)
	file = file.replace(" ", "©")
	command = "python PPTX_to_PDF.py " + file + " " + now
	res = os.system(command)  # открываем скрипт для форматирования
	file = file.replace("©", " ")
	doc = open('./GENERATED_PDF/' + now + '/' + file + ".pdf", 'rb')
	await message.reply_document(doc)

	connect = sqlite3.connect('users.db')
	cursor = connect.cursor()
	cursor.execute("""CREATE TABLE IF NOT EXISTS users(
			user_id TEXT PRIMARY KEY,
			user_name TEXT,
			date TEXT,
			time TEXT,
			source TEXT,
			uname_source TEXT,
			uid_source TEXT
   			)
    		""")	
	now_time = datetime.datetime.now()
	users_list = [UID, message.text, now, now_time.strftime("%H:%M:%S"), "Telegram", message.from_user.username, message.from_user.id]
	cursor.execute("INSERT INTO users VALUES(?,?,?,?,?,?,?);", users_list)
	connect.commit()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)