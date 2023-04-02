import logging

from parsers import get_all_pages
from adding_chapters import adding_chapters, adding_user_to_book, adding_link,adding_book_to_user, get_name_from_link
import database.sql_start
from create_bot import bot, dp
from keyboards import Close

async def adding_to_the_queue(user_id, link):
    database.sql_start.cur_Link.execute(f"""SELECT user_id,link FROM 'user_requests' WHERE user_id =? AND link =?""", (user_id, link))
    if database.sql_start.cur_Link.fetchone() is None:
        database.sql_start.cur_Link.execute(""" INSERT INTO 'user_requests' (user_id, link) VALUES(?,?) """, (user_id, link))
    else:
        print("Такой запрос есть")
    database.sql_start.base_Link.commit()


async def query_processing():
    database.sql_start.cur_Link.execute(""" SELECT * FROM 'user_requests' """)
    requests = database.sql_start.cur_Link.fetchall()
    for request in requests:
        #ДОБАВИТЬ ОБРАБОТКУ НЕКОРРЕКТНЫХ ССЫЫЛОК
        logging.info(f"Новый запрос от {request[0]} --- {request[1]}")
        info = database.sql_start.cur_Link.execute(f"""SELECT link FROM 'link' WHERE link = ?""", (request[1],))
        if info.fetchone() is None:
            try:
                name, list, photo = await get_all_pages(request[1])
            except:
                await bot.send_message(request[0], f"Ошибка при обработке ссылки - {request[1]}", reply_markup=Close)
                continue
            await adding_link(name, request[1], photo)
            await adding_chapters(name, list)
            await adding_user_to_book(request[0], request[1])
            await adding_book_to_user(request[0], request[1])

            photo = open(f"database/images/{name}.jpg", 'rb')
            await bot.send_photo(chat_id=request[0], photo = photo, caption=f"Книга добавлена!\n{name}", reply_markup=Close)
        else:
            name = await get_name_from_link(request[1])
            await adding_user_to_book(request[0], request[1])
            await adding_book_to_user(request[0], request[1])

            photo = open(f"database/images/{name}.jpg", 'rb')
            await bot.send_photo(chat_id=request[0], photo = photo, caption=f"Книга добавлена!\n{name}", reply_markup=Close)
    database.sql_start.cur_Link.execute(""" DELETE FROM 'user_requests' """)
    database.sql_start.base_Link.commit()

