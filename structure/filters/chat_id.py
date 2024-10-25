from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from loader import config


class ChatIDFilter(BaseFilter):
    async def __call__(self, event: Message | CallbackQuery) -> bool:
        if isinstance(event, Message):
            return event.chat.id == config.chats.QA_CHAT_ID
        elif isinstance(event, CallbackQuery):
            return event.message.chat.id == config.chats.QA_CHAT_ID
        return False
