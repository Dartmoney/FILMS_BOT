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

# подключаемся к локальному АПИ телеграм
local_server = TelegramAPIServer.from_base('http://localhost:22')
# передаем значение токена
API_TOKEN = API
# хранение всего в Оперативке (после перезагрузки все состояния для бота стираются)
storage = MemoryStorage()
# Создаем логгинг
logging.basicConfig(level=logging.INFO)
# Инициализируем бота и диспетчер
bot = Bot(token=API_TOKEN, server=local_server)
dp = Dispatcher(bot, storage=storage)
opisanie = False
# текущее зеркало hdrezka
tek_miror = "http://hdrezkadkrrq2.net"


# команда старт
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup()
    await message.reply("Мир вам")


# команда для поиска по имени
@dp.message_handler(commands=["search_name"])
async def chto(message: types.Message):
    global opisanie
    opisanie = False
    await message.reply("По названию")


# команда для поиска по описанию
@dp.message_handler(commands=["search_opisanie"])
async def kto(message: types.Message):
    global opisanie
    opisanie = True
    await message.reply("По описанию")


# команда для поиска рандомного фильма
@dp.message_handler(commands=["random"])
async def random(message: types.Message):
    global res
    # список для результата
    res = []
    # Подключение к бд
    con = sqlite3.connect("Triangle_Kino.db")
    cur = con.cursor()
    # запрос в бд
    result = cur.execute(f"""
                                                SELECT * FROM Triangle_Kino 
                                                ORDER BY RANDOM()
                                                LIMIT 1
                                                """)
    # цикл для редактирования и занесения данных в список
    for i in result:
        print(i)
        # добавление в список ответа и изменение ссылки с поправкой на текущее зеркало
        res.append([i[0], i[2], i[3], (tek_miror + "/films/" + i[4].split("/films/")[1])])
    # создание инлайн клавиатуры
    kbM = types.InlineKeyboardMarkup(row_width=1)
    # добавлени кнопки для скачивания фильма
    downloads = types.InlineKeyboardButton(text="скачать", callback_data="downloads")
    # добавление кнопки в клавиатуру
    kbM.add(downloads)
    con.commit()
    con.close()
    # отправка сообщения пользователю
    await message.reply(res[0][1] + " " + res[0][2] + " " + res[0][3], reply_markup=kbM)

    # обработчик нажатия на кнопку скачивания
    @dp.callback_query_handler(text="downloads")
    async def dowmloads(query: types.CallbackQuery):
        global res
        global kbM
        options = Options()
        options.add_argument("--headless")
        # указание местоположения хромдрайвера
        driver = webdriver.Chrome(options=options, executable_path="home/dartmoney/MY_BOT/FILMS_BOT/chromedriver")
        # запрос
        driver.get(res[0][3])
        oshibka = True
        try:
            # Просматриваем все запросы которые делает сайт и находим среди них прямую ссылку на фильм
            for request in driver.requests:
                if request.response:
                    if ".stream.voidboost.cc/" in request.url:
                        # скачивание фильма
                        urllib.request.urlretrieve((((request.url).split("mp4"))[0] + "mp4"),
                                                   "/tmpfs/" + str(query.message.chat.id) + ".mp4")
                        # делаем паузу что бы не схватить бан
                        time.sleep(60)
                        break
        except:
            #  в случае ошибки даем ответ пользователь об ошибке
            oshibka = False
            await query.message.reply("ошибка")
        # закрываем драйвер
        driver.quit()
        # в случае если ошибки нет отправляем фильм пользователю
        if oshibka:
            video = open("/tmpfs/" + str(query.message.chat.id) + ".mp4", 'rb')
            await bot.send_video(chat_id=query.message.chat.id, video=video)
            video.close()
            Path.unlink(Path("/tmpfs/" + str(query.message.chat.id) + ".mp4"))
            time.sleep(60)

# условие припоискуе по описанию
if opisanie:
    # спсиок для получения ответов с бд
    res = []
    k = 0
    #  Инлайн клавиатура
    kbM = types.InlineKeyboardMarkup(row_width=5)
    # кнопка которая отправляет пользователя к первому фильму
    first = types.InlineKeyboardButton(text='<<', callback_data="perv")
    #  кнопка отправляет пользователя к предыдущему фильму
    pred = types.InlineKeyboardButton(text="<", callback_data="pred")
    # кнопка для скачивания фильма
    download = types.InlineKeyboardButton(text="скачать", callback_data="download")
    # кнопка для перехода к следующему фильму
    sled = types.InlineKeyboardButton(text=">", callback_data="sled")
    # кнопка для перехода к последнему фильму
    posl = types.InlineKeyboardButton(text=">>", callback_data="posl")
    # добавление всех кнопок в клавиатуру
    kbM.add(first, pred, download, sled, posl)


    # обработчик при получении сообщения
    @dp.message_handler()
    async def message_from(message: types.Message):
        global res
        global k
        global kbM
        global tek_miror
        # текст сообщения
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


    # обработчик при нажатии кнопки следующего фильма
    @dp.callback_query_handler(text="sled")
    async def sled(query: types.CallbackQuery):
        global res
        global k
        global kbM
        k += 1
        if k < len(res):
            await query.message.edit_text(res[k][1] + " " + res[k][2] + " " + res[k][3], reply_markup=kbM)


    # кнопка для предыдущего фильма
    @dp.callback_query_handler(text="pred")
    async def pred(query: types.CallbackQuery):
        global res
        global k
        global kbM
        if (k - 1) >= 0:
            k -= 1
            await query.message.edit_text(res[k][1] + " " + res[k][2] + " " + res[k][3], reply_markup=kbM)


    # кнопка для первого фильма
    @dp.callback_query_handler(text="perv")
    async def perv(query: types.CallbackQuery):
        global res
        global k
        global kbM
        k = 0
        await query.message.edit_text(res[k][1] + " " + res[k][2] + " " + res[k][3], reply_markup=kbM)


    # кнопка для последнего фильма
    @dp.callback_query_handler(text="posl")
    async def posl(query: types.CallbackQuery):
        global res
        global k
        global kbM
        k = len(res) - 1
        await query.message.edit_text(res[k][1] + " " + res[k][2] + " " + res[k][3], reply_markup=kbM)


    # кнопка для скачивания
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
# то же самое только для поиска фильма по названию
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
