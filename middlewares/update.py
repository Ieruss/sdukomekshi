from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from typing import Callable, Dict, Any, Awaitable
from database.engine import Database


class UpdateUserMiddleware(BaseMiddleware):
    def __init__(self, db: Database):
        self.db = db
        super().__init__()

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        user_id = None
        if isinstance(event, Message):
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id
        if user_id:
            await self.db.user.update_activity(user_id)
        return await handler(event, data)
