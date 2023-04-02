import database.sql_start, os


async def delete_from_user_base(user_id, name_book): #user_books
    database.sql_start.cur_UserBooks.execute(f""" DELETE FROM '{user_id}' WHERE book_name =? """, (name_book,))

    count = database.sql_start.cur_UserBooks.execute(f""" SELECT COUNT(*) FROM '{user_id}' """).fetchone()[0]
    if int(count) == 0:
        database.sql_start.cur_UserBooks.execute(f""" DROP TABLE IF EXISTS '{user_id}' """)
    database.sql_start.base_UserBooks.commit()


async def delete_users_from_book(user_id, name_book): #book_users
    database.sql_start.cur_BookUsers.execute(f""" DELETE FROM '{name_book}' WHERE user_id=? """, (user_id,))
    database.sql_start.base_BookUsers.commit()
    count = database.sql_start.cur_BookUsers.execute(f""" SELECT COUNT(*) FROM '{name_book}' """).fetchone()[0]
    if int(count) == 0:
        database.sql_start.cur_ChapterLists.execute(f""" DROP TABLE IF EXISTS '{name_book}' """)
        database.sql_start.cur_BookUsers.execute(f""" DROP TABLE IF EXISTS '{name_book}' """)
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), f'database/images/{name_book}.jpg')
        os.remove(path)
        await delete_book_links(name_book)
        database.sql_start.base_ChapterLists.commit()


async def delete_book_links(name_book): #link_base
    database.sql_start.cur_Link.execute(f""" DELETE FROM 'link' WHERE name=? """, (name_book,))
    database.sql_start.base_Link.commit()


async def delete(user_id, name_book):
    await delete_from_user_base(user_id, name_book)
    await delete_users_from_book(user_id, name_book)