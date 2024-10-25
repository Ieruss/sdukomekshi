from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from typing import Callable, Dict, Any, Awaitable
from database.engine import Database
from parsing.login import login_user


class AuthCheckerMiddleware(BaseMiddleware):
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
        status = await self.db.user.get_status(user_id)
        command = event.text.split()[0]

        if status != 'registered':
            return await handler(event, data)

        username, password = await self.db.user.get_login_password(user_id)
        if username is None or password is None:
            return await handler(event, data)

        if command not in ['/attendance', '/grade', '/schedule']:
            return await handler(event, data)

        if not await login_user(username, password):
            await self.db.user.set_status(user_id, 'unregistered')
            await event.answer("❗️You can't use this command./n/n You must /start the bot again")
            return

        return await handler(event, data)
