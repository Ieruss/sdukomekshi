from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject, Message
from typing import Callable, Dict, Any, Awaitable
from database.engine import Database


class PermissionMiddleware(BaseMiddleware):
    def __init__(self, db: Database):
        self.db = db
        super().__init__()

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        if not isinstance(event, Message):
            return await handler(event, data)

        user_id = event.from_user.id
        command = event.text.strip().split()[0]
        status = await self.db.user.get_status(user_id)
        state: FSMContext = data.get('state')

        if command[0] != '/' or command == '/start':
            return await handler(event, data)

        if status is None or status != 'registered':
            await state.clear()
            await event.answer('‼️ You are not registered.\n\nPlease, use /start command to register')
            return

        return await handler(event, data)
