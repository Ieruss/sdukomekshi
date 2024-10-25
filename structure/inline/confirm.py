from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv.main import rewrite

confirm_keyword = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='✅', callback_data='send'),
         InlineKeyboardButton(text='❌', callback_data='cancel')]
    ]
)

qa_confirm_keyword = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='✅', callback_data='qa_send'),
         InlineKeyboardButton(text='❌', callback_data='qa_cancel')]
    ]
)

question_confirm_keyword = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='✅', callback_data='q_send'),
         InlineKeyboardButton(text='❌', callback_data='q_cancel')]
    ]
)
