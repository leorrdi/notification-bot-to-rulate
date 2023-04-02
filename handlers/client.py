from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import database.sql_start
from keyboards import MainMenu, Paging, books_callback, get_books_keyboard, BackMenu
from create_bot import dp, bot
from adding_and_processing_queue import adding_to_the_queue
from removal_from_database import delete

storage = MemoryStorage()


class Link(StatesGroup):
    link = State()


async def command_start(id):
    photoMainMenu = open("database/images/RULATE.jpg", "rb")
    await bot.send_photo(id, photo=photoMainMenu , caption="Выберите действие", reply_markup=MainMenu)


async def return_menu(callback: types.callback_query, text):
    photoMainMenu = open("database/images/RULATE.jpg", "rb")
    photoMainMenu = types.InputMedia(type="photo", media=photoMainMenu, caption=f'{text}')
    await callback.message.edit_media(media=photoMainMenu, reply_markup=MainMenu)


async def command_add_book(callback: types.callback_query):
    await Link.link.set()
    await bot.send_message(callback.from_user.id, "Введите ссылку", reply_markup=BackMenu)


async def load_link(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['link'] = message.text
    await adding_to_the_queue(user_id=int(message.from_user.id), link=data['link'])
    await command_start(message.from_user.id)
    await state.finish()


async def cancel_handler(message: types.message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
    await command_start(message.from_user.id)


async def cancel(callback: types.callback_query):
    await return_menu(callback, "Выберите действие")


async def delete_message(callback: types.callback_query):
    await callback.message.delete()


async def display_list_books(callback: types.callback_query):
    database.sql_start.cur_UserBooks.execute(f""" SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{callback.from_user.id}' """)
    if database.sql_start.cur_UserBooks.fetchone()[0] == 0:
        await return_menu(callback, "Вы еще не добавили ни одной книги")
        return
    list_books = database.sql_start.cur_UserBooks.execute(f""" SELECT * FROM '{callback.from_user.id}' """).fetchall()
    book = list_books[0][0]
    photo = open(f"database/images/{list_books[0][0]}.jpg", "rb")
    photo = types.InputMedia(type="photo", media=photo, caption=book)
    keyboard = await get_books_keyboard(len=len(list_books))
    await callback.message.edit_media(media=photo, reply_markup=keyboard)


async def delete_book(callback: types.callback_query):
    await delete(str(callback.from_user.id), str(callback.message.caption))
    await display_list_books(callback)


@dp.callback_query_handler(books_callback.filter())
async def book_page_handler(query: types.callback_query, callback_data: dict):
    page = int(callback_data.get("page"))
    list_books = database.sql_start.cur_UserBooks.execute(f""" SELECT * FROM '{query.from_user.id}' """).fetchall()
    book_data = list_books[page][0]
    caption = f"{book_data}"
    keyboard = await get_books_keyboard(page, len(list_books))

    photo = open(f"database/images/{book_data}.jpg", "rb")
    photo = types.InputMedia(type="photo", media=photo, caption=caption)

    await query.message.edit_media(photo, keyboard)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_callback_query_handler(command_add_book, text='add_book')
    dp.register_callback_query_handler(delete_book, text='delete')
    dp.register_callback_query_handler(cancel, text='back')
    dp.register_callback_query_handler(delete_message, text='delete_message')
    dp.register_message_handler(cancel_handler, state="*", text='Главное меню')
    dp.register_callback_query_handler(display_list_books, text='show_book')

    dp.register_message_handler(load_link, state=Link.link)
