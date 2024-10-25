from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv.main import rewrite

login_keyword = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Login', callback_data='login'),]
    ]
)

rewrite_login_keyword = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='🔄 Rewrite', callback_data='rewrite_login'),]
    ]
)