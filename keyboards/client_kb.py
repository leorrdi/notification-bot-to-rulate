from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

MainMenu = InlineKeyboardMarkup(row_width=1)
addButton = InlineKeyboardButton(text='Добавить книгу', callback_data='add_book')
showButton = InlineKeyboardButton(text='Список книг', callback_data='show_book')
MainMenu.add(addButton,showButton)


BackMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
BackButton = KeyboardButton(text = 'Главное меню')
BackMenu.add(BackButton)

Close = InlineKeyboardMarkup(row_width=1)
close = InlineKeyboardButton(text='Закрыть', callback_data='delete_message')
Close.add(close)

Paging = InlineKeyboardMarkup(row_width=2)
nextButton = InlineKeyboardButton(text='➡️', callback_data='next')
previousButton = InlineKeyboardButton(text='⬅️', callback_data='previous')
deleteButton = InlineKeyboardButton(text='Удалить', callback_data='delete')
closeButton = InlineKeyboardButton(text='Закрыть', callback_data='back')
Paging.add(previousButton, nextButton).add(deleteButton)
books_callback = CallbackData("Books", "page")


async def get_books_keyboard(page: int = 0, len: int = 0) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    row_btns = []
    has_next_page = len > page + 1

    if page != 0:
        row_btns.append(
            InlineKeyboardButton(
                text="⬅️️️️️",
                callback_data=books_callback.new(page=page - 1)
            )
        )
    else:
        row_btns.append(
            InlineKeyboardButton(
                text="↪️",
                callback_data=books_callback.new(page=len-1)
            )
        )

    if has_next_page:
        row_btns.append(
            InlineKeyboardButton(
                text="➡️",
                callback_data=books_callback.new(page=page + 1)
            )
        )
    else:
        row_btns.append(
            InlineKeyboardButton(
                text="↩️",
                callback_data=books_callback.new(page=0)
            )
        )

    keyboard.row(*row_btns).add(deleteButton).add(closeButton)
    return keyboard