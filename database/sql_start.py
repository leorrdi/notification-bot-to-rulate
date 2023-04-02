import sqlite3

global cur_Link, base_Link
global cur_ChapterLists, base_ChapterLists
global cur_UserBooks, base_UserBooks
global cur_BookUsers, base_BookUsers


def sql_start():
    global cur_Link, base_Link
    base_Link = sqlite3.connect('database/link_base.db')
    cur_Link = base_Link.cursor()
    base_Link.execute("""CREATE TABLE IF NOT EXISTS 'user_requests'(
        user_id TEXT,
        link TEXT,
        UNIQUE(user_id, link)
        )""")
    base_Link.commit()
    base_Link.execute(""" CREATE TABLE IF NOT EXISTS 'link'(name TEXT, link TEXT, photo TEXT) """)
    base_Link.commit()

    global cur_ChapterLists, base_ChapterLists
    base_ChapterLists = sqlite3.connect('database/chapter_lists.db')
    cur_ChapterLists = base_ChapterLists.cursor()
    base_ChapterLists.commit()

    global cur_UserBooks, base_UserBooks
    base_UserBooks = sqlite3.connect('database/user_books.db')
    cur_UserBooks = base_UserBooks.cursor()
    base_UserBooks.commit()

    global cur_BookUsers, base_BookUsers
    base_BookUsers = sqlite3.connect('database/book_users.db')
    cur_BookUsers = base_BookUsers.cursor()
    base_BookUsers.commit()