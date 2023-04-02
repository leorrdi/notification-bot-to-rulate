import asyncio

import requests
from bs4 import BeautifulSoup


async def get_all_pages(url: str):
    await asyncio.sleep(2)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/107.0.0.0 Safari/537.36 "
    }
    req = requests.get(url=url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, "lxml")
    list_of_chapters = []

    name = soup.find(class_="span8").find('h1').text.split('/')[-1].strip()
    photo_req = requests.get("https://tl.rulate.ru" + soup.find(class_='images').find(class_="slick").find("img")["src"]).content
    photo = f"database/images/{name}.jpg"
    with open(photo, 'wb') as handler:
        handler.write(photo_req)

    all_chapters = soup.find(class_="table table-condensed table-striped").findAll(class_=["chapter_row"])

    for item in all_chapters:
        chapter_name = item.find(class_="t").find('a').text
        link = "https://tl.rulate.ru" + item.find(class_="t").find('a').get('href')
        status = item.findAll('td')[-5].text

        list_of_chapters.append(
            (
                chapter_name.strip(), link.strip(), status.strip()
                #"chapter_name": chapter_name,
                #"chapter_link": link
            )
        )
    return name, list_of_chapters, photo
