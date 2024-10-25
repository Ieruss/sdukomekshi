from functools import wraps

from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from database.models import UserModel

def with_session(funct):
    @wraps(funct)
    async def wrapper(self, *args, **kwargs):
        session = kwargs.get('session', None)
        if session is None:
            async with self.session_pool() as session:
                return await funct(self, session, *args, **kwargs)
        else:
            return await funct(self, session, *args, **kwargs)

    return wrapper

class UserStatisticsClass:

    def __init__(self, session_pool):
        self.session_pool = session_pool

    @with_session
    async def get_total_users(self, session: AsyncSession) -> int:
        result = await session.execute(select(func.count()).select_from(UserModel))
        return result.scalar()

    @with_session
    async def get_registered_users(self, session: AsyncSession) -> int:
        result = await session.execute(select(func.count()).select_from(UserModel).where(UserModel.status == 'registered'))
        return result.scalar()

    @with_session
    async def get_banned_users(self, session: AsyncSession) -> int:
        result = await session.execute(select(func.count()).select_from(UserModel).where(UserModel.status == 'banned'))
        return result.scalar()

    @with_session
    async def get_unlogged_users(self, session: AsyncSession) -> int:
        result = await session.execute(select(func.count()).select_from(UserModel).where(UserModel.username == None))
        return result.scalar()

    @with_session
    async def get_active_users(self, session: AsyncSession, time_delta: timedelta) -> int:
        time_threshold = datetime.utcnow() + timedelta(hours=5) - time_delta
        result = await session.execute(
            select(func.count()).select_from(UserModel).where(UserModel.updated >= time_threshold)
        )
        return result.scalar()

    @with_session
    async def calc(self, session: AsyncSession) -> dict:
        return {
            "total_users": await self.get_total_users(),
            "registered_users": await self.get_registered_users(),
            "banned_users": await self.get_banned_users(),
            "unlogged_users": await self.get_unlogged_users(),
            "active_last_hour": await self.get_active_users(time_delta=timedelta(hours=1)),
            "active_last_6_hours": await self.get_active_users(time_delta=timedelta(hours=6)),
            "active_last_day": await self.get_active_users(time_delta=timedelta(days=1)),
            "active_last_week": await self.get_active_users(time_delta=timedelta(weeks=1)),
        }
