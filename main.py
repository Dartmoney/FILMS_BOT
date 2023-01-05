from bs4 import BeautifulSoup
import requests
import random
import sqlite3
from seleniumwire import webdriver  # Import from seleniumwire
from selenium.webdriver.chrome.options import Options

db = sqlite3.connect("Triangle_Kino.db")
cur = db.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS Triangle_Kino (
    ID INTEGER PRIMARY KEY,
    RESURS TEXT,
    NAME TEXT,
    OPISANIE TEXT,
    LINK_STR TEXT
)""")
db.commit()

resursZERO = "HDREZKA"

user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]

user_agent = random.choice(user_agent_list)
headers = {'User-Agent': user_agent}

x = 1

url = "http://hdrezkabbsm2k.net/?filter=last&genre=1"
req = list()
while True:
    i = 0
    page = BeautifulSoup(requests.get(url, headers=headers).text, "lxml")

    name_list = []
    link1_list = []
    opisanie_list = []
    for name in page.find_all("div", class_="b-content__inline_item-link"):
        name_text = name.text
        url = name.find_all('a')[0].get("href")
        print(name_text)
        print(url)
        link1_list.append(url)
        name_list.append(name_text)

    for link0 in link1_list:
        page2 = BeautifulSoup(requests.get(link0, headers=headers).text, "lxml")
        opisanie = page2.find("div", class_="b-post__description_text").text

        print(opisanie)

        options = Options()
        options.add_argument("--headless")

        driver = webdriver.Chrome(options=options)

        # Go to the Google home page
        driver.get(link0)
        # Access requests via the `requests` attribute
        for request in driver.requests:
            if request.response:
                if "http://stream.voidboost.cc/" in request.url:
                    req.append(
                        request.url
                    )

        opisanie_list.append(opisanie)
    while i < len(opisanie_list):
        name1 = name_list[i]
        opisanie1 = opisanie_list[i]
        link2 = req[i]

        cur.execute("""INSERT INTO Triangle_Kino (RESURS, NAME, OPISANIE, LINK_STR) VALUES (?, ?, ?, ?);""",
                    (resursZERO, name1, opisanie1, link2))
        db.commit()
        print("Добавлено " + str(i))
        i = i + 1

    x = x + 1

    url = f"http://hdrezkabbsm2k.net/{str(x)}/?filter=last&genre=1"

    if x == 1008:
        break
