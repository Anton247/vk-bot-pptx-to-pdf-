import datetime
import uuid
import os
from sqlite3.dbapi2 import Cursor
from PPTX_GENERATOR import PPTX_GENERATOR 
import sqlite3

import logging
from vkbottle.bot import Bot, Message
from setting import TOKEN

logging.basicConfig(level="DEBUG")

bot = Bot(token=TOKEN)

@bot.on.message(text="Начать")
async def hi_handler(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    S = "Привет, {}".format(users_info[0].first_name)
    S += "\n👋🏼😀\nЯ Квантоша, бот, созданный для отправки сертификата о посещении дня открытых дверей\
        Напиши мне своё имя и я отправлю тебе твой сертификат"
    await message.answer(S)

bot.run_forever()


