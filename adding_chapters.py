import database.sql_start


async def adding_chapters(name_book, list): #chapter_lists
    query = f""" CREATE TABLE IF NOT EXISTS '{name_book}' (
    chapter_name TEXT,
    chapter_link TEXT,
    chapter_status TEXT,
    UNIQUE(chapter_name, chapter_link)
    )"""
    database.sql_start.cur_ChapterLists.execute(query)

    query = f""" INSERT INTO '{name_book}' (chapter_name, chapter_link, chapter_status) VALUES(?,?,?) """
    database.sql_start.cur_ChapterLists.executemany(query, list)
    database.sql_start.base_ChapterLists.commit()


async def adding_user_to_book(user_id, link): #user_books
    book_name = await get_name_from_link(link)
    query = f""" CREATE TABLE IF NOT EXISTS '{str(user_id)}' (
    book_name TEXT,
    UNIQUE(book_name)
    ) """
    database.sql_start.cur_UserBooks.execute(query)

    database.sql_start.cur_UserBooks.execute(f""" INSERT OR IGNORE INTO '{str(user_id)}' (book_name) VALUES(?) """, (book_name,))
    database.sql_start.base_UserBooks.commit()


async def adding_book_to_user(book_user, link): # book_users
    book_name = await get_name_from_link(link)

    query = f""" CREATE TABLE IF NOT EXISTS '{book_name}' (
    user_id TEXT,
    UNIQUE(user_id)
    ) """
    database.sql_start.cur_BookUsers.execute(query)

    database.sql_start.cur_BookUsers.execute(f""" INSERT OR IGNORE INTO '{book_name}' (user_id) VALUES(?) """, (book_user,))
    database.sql_start.base_BookUsers.commit()


async def adding_link(name, link, photo): #link_base
    database.sql_start.cur_Link.execute(""" INSERT INTO 'link' (name, link, photo) VALUES(?,?,?) """, (name, link, photo))
    database.sql_start.base_Link.commit()


async def get_name_from_link(link): #link_base
        database.sql_start.cur_Link.execute(""" SELECT name FROM 'link' WHERE link = ? """, (link,))
        a = database.sql_start.cur_Link.fetchone()
        return a[0]