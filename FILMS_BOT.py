from MY_API import API
import logging
import sqlite3
from aiogram import Bot, Dispatcher, executor, types
import random

API_TOKEN = API

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
opisanie = False


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply("Мир вам")


@dp.message_handler(commands=['поиск_по_названию_или_по_году'])
async def search_name(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    opisanie = False
    await message.reply("напиши название или год")


@dp.message_handler(commands=['поиск_по_описанию'])
async def search_opisanie(message: types.Message):
    opisanie = True
    await message.reply("напиши описание")


if not opisanie:
    @dp.message_handler()
    async def message_from(message: types.Message):
        p = message.text
        con = sqlite3.connect("Triangle_Kino.db")
        cur = con.cursor()
        result = cur.execute(f"""
                            SELECT * FROM Triangle_Kino 
                            WHERE NAME LIKE "%{p}%"
                            """)
        for i in result:
            await message.reply(i)
        con.commit()
        con.close()
else:
    @dp.message_handler()
    async def message_from(message: types.Message):
        p = message.text
        con = sqlite3.connect("Triangle_Kino.db")
        cur = con.cursor()
        result = cur.execute(f"""
                                    SELECT * FROM Triangle_Kino 
                                    WHERE OPISANIE LIKE "%{p}%"
                                    """)
        for i in result:
            print(i)
        con.commit()
        con.close()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
