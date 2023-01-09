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


@dp.message_handler(commands=['поиск по названию'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("напиши название")

if not opisanie:
    @dp.message_handler()
    async def message_from(message: types.Message):
        p = message.text
        con = sqlite3.connect("Triangle_Kino.db")
        cur = con.cursor()
        cur.execute("""
                            SELECT FROM films 
                            WHERE genre = (SELECT id FROM genres WHERE title ='комедия' )
                            """)
        con.commit()
        con.close()
# driver = webdriver.Chrome(options=options,executable_path="home/dartmoney/MY_BOT/FILMS_BOT/chromedriver")
#         # Go to the Google home page
#                 driver.get(link0)
#         # Access requests via the `requests` attribute
#                 for request in driver.requests:
#                     if request.response:
#                         if ".stream.voidboost.cc/" in request.url:
#                             req.append(
#                                 request.url
#                             )
#                 time.sleep(0.01)
#                 driver.quit()
#                 opisanie_list.append(opisanie)
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
