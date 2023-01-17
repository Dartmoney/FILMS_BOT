import time
from pathlib import Path
from MY_API import API
import logging
import sqlite3
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import random
import requests
from bs4 import BeautifulSoup
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
import urllib.request
from aiogram.bot.api import TelegramAPIServer

Path("/home/dartmoney/MY_BOT/FILMS_BOT/tmpfs").mkdir(parents=True, exist_ok=True)
local_server = TelegramAPIServer.from_base('http://localhost:22')
API_TOKEN = API
storage = MemoryStorage()
# Configure logging
logging.basicConfig(level=logging.INFO)
# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN, server=local_server)
dp = Dispatcher(bot, storage=storage)
opisanie = False
tek_miror = "http://hdrezkadkrrq2.net"


def get_free_proxies():
    url = "https://free-proxy-list.net/"
    # получаем ответ HTTP и создаем объект soup
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    k = soup.find("table", class_="table table-striped table-bordered")
    proxies = []
    p = 0
    for j in k.find_all("tr")[1:]:
        row_data = j.find_all("td")
        row = [row_data[i].text for i in range(2)]
        proxies.append(":".join(row))
    return proxies


# sdssdds
def get_session(proxies):
    # создать HTTP‑сеанс
    session = requests.Session()
    # выбираем один случайный прокси
    proxy = random.choice(proxies)
    session.proxies = {"http": proxy, "https": proxy}

    return proxy, session


proxy = get_free_proxies()


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup()
    await message.reply("Мир вам")


@dp.message_handler(commands=["search_name"])
async def chto(message: types.Message):
    global opisanie
    opisanie = False
    await message.reply("По названию")


@dp.message_handler(commands=["search_opisanie"])
async def kto(message: types.Message):
    global opisanie
    opisanie = True
    await message.reply("По описанию")


@dp.message_handler(commands=["random"])
async def random(message: types.Message):
    global res
    res = []
    con = sqlite3.connect("Triangle_Kino.db")
    cur = con.cursor()
    result = cur.execute(f"""
                                                SELECT * FROM Triangle_Kino 
                                                ORDER BY RANDOM()
                                                LIMIT 1
                                                """)
    for i in result:
        print(i)
        res.append([i[0], i[2], i[3], (tek_miror + "/films/" + i[4].split("/films/")[1])])
    kbM = types.InlineKeyboardMarkup(row_width=1)
    downloads = types.InlineKeyboardButton(text="скачать", callback_data="downloads")
    kbM.add(downloads)
    con.commit()
    con.close()
    await message.reply(res[0][1] + " " + res[0][2] + " " + res[0][3], reply_markup=kbM)

    @dp.callback_query_handler(text="downloads")
    async def dowmloads(query: types.CallbackQuery):
        global res
        global kbM
        options = Options()
        options.add_argument("--headless")
        # Go to the Google home page
        driver = webdriver.Chrome(options=options, executable_path="home/dartmoney/MY_BOT/FILMS_BOT/chromedriver")
        print(res)
        driver.get(res[0][3])
        print("vse ese est")
        oshibka = True
        try:
            # Access requests via the `requests` attribute
            for request in driver.requests:
                if request.response:
                    if ".stream.voidboost.cc/" in request.url:
                        urllib.request.urlretrieve((((request.url).split("mp4"))[0] + "mp4"),
                                                   "/tmpfs/" + str(query.message.chat.id) + ".mp4")
                        time.sleep(60)
                        break
        except:
            oshibka = False
            await query.message.reply("ошибка")
        driver.quit()
        if oshibka:
            video = open("/tmpfs/" + str(query.message.chat.id) + ".mp4", 'rb')
            await bot.send_video(chat_id=query.message.chat.id, video=video)
            video.close()
            Path.unlink(Path("/tmpfs/" + str(query.message.chat.id) + ".mp4"))
            time.sleep(60)


if opisanie:
    res = []
    k = 0
    kbM = types.InlineKeyboardMarkup(row_width=5)
    first = types.InlineKeyboardButton(text='<<', callback_data="perv")
    pred = types.InlineKeyboardButton(text="<", callback_data="pred")
    download = types.InlineKeyboardButton(text="скачать", callback_data="download")
    sled = types.InlineKeyboardButton(text=">", callback_data="sled")
    posl = types.InlineKeyboardButton(text=">>", callback_data="posl")
    kbM.add(first, pred, download, sled, posl)


    @dp.message_handler()
    async def message_from(message: types.Message):
        global res
        global k
        global kbM
        global tek_miror
        p = message.text
        con = sqlite3.connect("Triangle_Kino.db")
        cur = con.cursor()
        result = cur.execute(f"""
                                            SELECT * FROM Triangle_Kino 
                                            WHERE OPISANIE LIKE ?""", ("%" + p + "%",))
        for i in result:
            res.append([i[0], i[2], i[3], (tek_miror + "/films/" + i[4].split("/films/")[1])])
        print(res)
        await message.reply(res[k][1] + " " + res[k][2] + " " + res[k][3], reply_markup=kbM)
        con.commit()
        con.close()


    @dp.callback_query_handler(text="sled")
    async def sled(query: types.CallbackQuery):
        global res
        global k
        global kbM
        k += 1
        if k < len(res):
            await query.message.edit_text(res[k][1] + " " + res[k][2] + " " + res[k][3], reply_markup=kbM)


    @dp.callback_query_handler(text="pred")
    async def pred(query: types.CallbackQuery):
        global res
        global k
        global kbM
        if (k - 1) >= 0:
            k -= 1
            await query.message.edit_text(res[k][1] + " " + res[k][2] + " " + res[k][3], reply_markup=kbM)


    @dp.callback_query_handler(text="perv")
    async def perv(query: types.CallbackQuery):
        global res
        global k
        global kbM
        k = 0
        await query.message.edit_text(res[k][1] + " " + res[k][2] + " " + res[k][3], reply_markup=kbM)


    @dp.callback_query_handler(text="posl")
    async def posl(query: types.CallbackQuery):
        global res
        global k
        global kbM
        k = len(res) - 1
        await query.message.edit_text(res[k][1] + " " + res[k][2] + " " + res[k][3], reply_markup=kbM)


    @dp.callback_query_handler(text="download")
    async def dowmload(query: types.CallbackQuery):
        global res
        global k
        global kbM
        options = Options()
        options.add_argument("--headless")
        # Go to the Google home page
        driver = webdriver.Chrome(options=options, executable_path="home/dartmoney/MY_BOT/FILMS_BOT/chromedriver")
        driver.get(res[k][3])
        oshibka = True
        try:
            # Access requests via the `requests` attribute
            for request in driver.requests:
                if request.response:
                    if ".stream.voidboost.cc/" in request.url:
                        urllib.request.urlretrieve((((request.url).split("mp4"))[0] + "mp4"),
                                                   "/tmpfs/" + str(query.message.chat.id) + ".mp4")
                        time.sleep(60)
                        break
        except:
            oshibka = False
            await query.message.reply("ошибка")
        driver.quit()
        if oshibka:
            video = open("/tmpfs/" + str(query.message.chat.id) + ".mp4", 'rb')
            await bot.send_video(chat_id=query.message.chat.id, video=video)
            video.close()
            Path.unlink(Path("/tmpfs/" + str(query.message.chat.id) + ".mp4"))
            time.sleep(60)

else:
    res = []
    k = 0
    kbM = types.InlineKeyboardMarkup(row_width=5)
    first = types.InlineKeyboardButton(text='<<', callback_data="perv")
    pred = types.InlineKeyboardButton(text="<", callback_data="pred")
    download = types.InlineKeyboardButton(text="скачать", callback_data="download")
    sled = types.InlineKeyboardButton(text=">", callback_data="sled")
    posl = types.InlineKeyboardButton(text=">>", callback_data="posl")
    kbM.add(first, pred, download, sled, posl)


    @dp.message_handler()
    async def message_from(message: types.Message):
        global res
        global k
        global kbM
        global tek_miror
        p = message.text
        con = sqlite3.connect("Triangle_Kino.db")
        cur = con.cursor()
        result = cur.execute(f"""
                                            SELECT * FROM Triangle_Kino 
                                            WHERE NAME LIKE ?""", ("%" + p + "%",))
        for i in result:
            res.append([i[0], i[2], i[3], (tek_miror + "/films/" + i[4].split("/films/")[1])])

        print(res)
        await message.reply(res[k][1] + " " + res[k][2] + " " + res[k][3], reply_markup=kbM)
        con.commit()
        con.close()


    @dp.callback_query_handler(text="sled")
    async def sled(query: types.CallbackQuery):
        global res
        global k
        global kbM
        k += 1
        if k < len(res):
            await query.message.edit_text(res[k][1] + " " + res[k][2] + " " + res[k][3], reply_markup=kbM)


    @dp.callback_query_handler(text="pred")
    async def pred(query: types.CallbackQuery):
        global res
        global k
        global kbM
        if (k - 1) >= 0:
            k -= 1
            await query.message.edit_text(res[k][1] + " " + res[k][2] + " " + res[k][3], reply_markup=kbM)


    @dp.callback_query_handler(text="perv")
    async def perv(query: types.CallbackQuery):
        global res
        global k
        global kbM
        k = 0
        await query.message.edit_text(res[k][1] + " " + res[k][2] + " " + res[k][3], reply_markup=kbM)


    @dp.callback_query_handler(text="posl")
    async def posl(query: types.CallbackQuery):
        global res
        global k
        global kbM
        k = len(res) - 1
        await query.message.edit_text(res[k][1] + " " + res[k][2] + " " + res[k][3], reply_markup=kbM)


    @dp.callback_query_handler(text="download")
    async def dowmload(query: types.CallbackQuery):
        global res
        global k
        global kbM
        options = Options()
        options.add_argument("--headless")
        # Go to the Google home page
        driver = webdriver.Chrome(options=options, executable_path="home/dartmoney/MY_BOT/FILMS_BOT/chromedriver")
        driver.get(res[k][3])
        oshibka = True
        try:
            # Access requests via the `requests` attribute
            for request in driver.requests:
                if request.response:
                    if ".stream.voidboost.cc/" in request.url:
                        urllib.request.urlretrieve((((request.url).split("mp4"))[0] + "mp4"),
                                                   "/tmpfs/" + str(query.message.chat.id) + ".mp4")
                        time.sleep(60)
                        break
        except:
            oshibka = False
            await query.message.reply("ошибка")
        driver.quit()
        if oshibka:
            video = open("/tmpfs/" + str(query.message.chat.id) + ".mp4", 'rb')
            await bot.send_video(chat_id=query.message.chat.id, video=video)
            video.close()
            Path.unlink(Path("/tmpfs/" + str(query.message.chat.id) + ".mp4"))
            time.sleep(60)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
