from bs4 import BeautifulSoup
import requests
import random
import sqlite3
from multiprocessing import Process
import time

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
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.119 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.119 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.119 Safari/537.36"
]

Tek_mirror = "http://hdrezka443rtt.net"


def req(k, x=0, url=f"{Tek_mirror}?filter=last&genre=1"):
    user_agent = random.choice(user_agent_list)

    while True:
        try:
            headers = {'User-Agent': user_agent}
            i = 0
            time.sleep(0.01)
            page = BeautifulSoup(requests.get(url, headers=headers).text, "lxml")
            name_list = []
            link1_list = []
            opisanie_list = []
        except:
            continue
        try:
            for name in page.find_all("div", class_="b-content__inline_item-link"):
                name_text = name.text
                url = name.find_all('a')[0].get("href")
                print(name_text)
                print(url)
                link1_list.append(url)
                name_list.append(name_text)
        except:
            continue
        for link0 in link1_list:
            try:
                time.sleep(0.01)
                page2 = BeautifulSoup(requests.get(link0, headers=headers).text, "lxml")
                opisanie = page2.find("div", class_="b-post__description_text").text
                print(opisanie)
            except:
                continue
        while i < len(opisanie_list):
            try:
                if not (((i + 1) < len(name_list)) and ((i + 1) < len(link1_list)) and ((i + 1) < len(opisanie_list))):
                    continue
                name1 = name_list[i]
                opisanie1 = opisanie_list[i]
                link2 = link1_list[i]
                cur.execute("""INSERT INTO Triangle_Kino (RESURS, NAME, OPISANIE, LINK_STR) VALUES (?, ?, ?, ?);""",
                            (resursZERO, name1, opisanie1, link2))
                db.commit()
                print("Добавлено " + str(i))
                i = i + 1
            except:
                continue
        x = x + 1
        url = f"{Tek_mirror}/page/{x}/?filter=last&genre=1"
        if x == k:
            break


if __name__ == '__main__':
    p1 = Process(target=req(100))
    p1.start()
    p2 = Process(target=req(200, x=101, url=f"{Tek_mirror}/page/101/?filter=last&genre=1"))
    p2.start()
    p3 = Process(target=req(300, x=201, url=f"{Tek_mirror}/page/201/?filter=last&genre=1"))
    p3.start()
    p4 = Process(target=req(400, x=301, url=f"{Tek_mirror}/page/301/?filter=last&genre=1"))
    p4.start()
    p5 = Process(target=req(500, x=401, url=f"{Tek_mirror}/page/401/?filter=last&genre=1"))
    p5.start()
    p6 = Process(target=req(600, x=501, url=f"{Tek_mirror}/page/501/?filter=last&genre=1"))
    p6.start()
    p7 = Process(target=req(700, x=601, url=f"{Tek_mirror}/page/601/?filter=last&genre=1"))
    p7.start()
    p8 = Process(target=req(800, x=701, url=f"{Tek_mirror}/page/701/?filter=last&genre=1"))
    p8.start()
    p9 = Process(target=req(900, x=801, url=f"{Tek_mirror}/page/801/?filter=last&genre=1"))
    p9.start()
    p10 = Process(target=req(1009, x=901, url=f"{Tek_mirror}/page/901/?filter=last&genre=1"))
    p10.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()
    p6.join()
    p7.join()
    p8.join()
    p9.join()
    p10.join()
