import asyncio
from aiogram.utils.markdown import hlink
from create_bot import dp, bot
import database.sql_start
from parsers import get_all_pages
from adding_chapters import adding_chapters
from keyboards import Close


async def update(): #link_base
    await asyncio.sleep(5)
    links = database.sql_start.cur_Link.execute(""" SELECT * FROM 'link' """).fetchall()
    for link in links:
        book_name = link[0]
        book_link = link[1]
        chapters_before_update = await get_chapters_before_update(book_name)
        name, updated_chapters, photo = await get_all_pages(book_link)

        new_chapters = []
        for i in updated_chapters: #Проверка новых глав
            flag = True
            for c in chapters_before_update:                #Отредактировать!!
                if c[1] == i[1]:
                    flag = False
                    break
            if flag:
                new_chapters.append(i)

        status_updated_chapters = []
        for i in updated_chapters: #Проверка новых статусов у глав
            for c in chapters_before_update:
                if (i[1] == c[1] and i[2] != c[2]):
                    status_updated_chapters.append(i)

        if len(new_chapters):
            await mailing(book_name, new_chapters, photo, "Вышла новая глава!")

        if len(status_updated_chapters):
            await mailing(book_name, status_updated_chapters,photo,"Статус главы изменился!")
        await rewriting_chapters(book_name, updated_chapters)


async def get_chapters_before_update(book_name): #chapter_lists
    return database.sql_start.cur_ChapterLists.execute(f""" SELECT * FROM '{book_name}' """).fetchall()


async def rewriting_chapters(book_name, update_chapters): #chapter_lists
    database.sql_start.cur_ChapterLists.execute(f""" DELETE FROM '{book_name}' """)
    await adding_chapters(book_name, update_chapters)


async def mailing(book_name, chapters, photo, text):  # Функция для рассылки
    users = database.sql_start.cur_BookUsers.execute(f""" SELECT * FROM '{book_name}' """).fetchall()
    for user in users:
        for chapter in chapters:
            text_link = hlink(f'{chapter[0]}', f'{chapter[1]}')
            photo = open(f"database/images/{book_name}.jpg", 'rb')
            await bot.send_photo(chat_id=user[0], photo=photo,
                                 caption=f"{book_name}\n\n{text}\n{text_link} - {chapter[2]}", parse_mode="HTML", reply_markup=Close)