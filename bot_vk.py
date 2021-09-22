# pip install aiofiles

import datetime
import uuid
import os
from sqlite3.dbapi2 import Cursor

from vkbottle.tools.dev_tools import keyboard
from PPTX_GENERATOR import PPTX_GENERATOR 
import sqlite3

import logging
from vkbottle.bot import Bot, Message
from vkbottle.tools import DocMessagesUploader
from setting import TOKEN

logging.basicConfig(level="DEBUG")

bot = Bot(token=TOKEN)

keyboard = '{"buttons":[[{"action":{"type":"text","label":"Хочу сертификат","payload":""},"color":"positive"}]]}'

@bot.on.message(text="Начать")
async def hi_handler(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    S = "Привет, {}".format(users_info[0].first_name)
    S += "\n👋🏼😀\nЯ Квантоша, бот, созданный для отправки сертификата о посещении дня открытых дверей\
        Напиши мне своё имя и я отправлю тебе твой сертификат"
    await message.answer(S, keyboard=keyboard)

@bot.on.message(text="Хочу сертификат")
async def what_is_name(message: Message):
    await message.answer("Напиши мне свои ФИО")

@bot.on.message()
async def certificate(message: Message):
    await message.answer("Твой сертификат создаётся, подожди немного", keyboard=keyboard)
    now = str(datetime.date.today().day)
    now += "-" + str(datetime.date.today().month)
    now += "-" + str(datetime.date.today().year)
    UID = uuid.uuid4().hex #уникальный идентификатор
    file = PPTX_GENERATOR(message.text, UID, now)
    print("GENERATOR OK")
    file = file.replace(" ", "©")
    command = "python PPTX_to_PDF.py " + file + " " + now
    print("открываем скрипт для форматирования")
    res = os.system(command)  # открываем скрипт для форматирования
    file = file.replace("©", " ")
    print("PDF OK")
    doc = await DocMessagesUploader(bot.api).upload(
        file + ".pdf", './GENERATED_PDF/' + now + '/' + file + ".pdf", peer_id=message.peer_id
    )
    print("DOK OK")
    await message.answer(attachment=doc)

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
    users_info = await bot.api.users.get(message.from_id)
    print("INFOOOOOOOOOOOO")
    print(users_info)
    users_list = [UID, message.text, now, now_time.strftime("%H:%M:%S"), "VK", users_info[0].first_name + " " + users_info[0].last_name, users_info[0].id]
    cursor.execute("INSERT INTO users VALUES(?,?,?,?,?,?,?);", users_list)
    connect.commit()

bot.run_forever()


