from aiogram.filters import BaseFilter
from aiogram.types import Message
from loader import config


class AdminFilter(BaseFilter):
    is_admin: bool = True

    async def __call__(self, obj: Message) -> bool:
        return (str(obj.from_user.id) in config.admins.list) == self.is_admin
