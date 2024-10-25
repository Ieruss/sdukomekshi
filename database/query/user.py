from functools import wraps


from sqlalchemy import select, delete, func, update
from sqlalchemy.ext.asyncio import AsyncSession

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


class UserClass:
    def __init__(self, session_pool):
        self.session_pool = session_pool

    @with_session
    async def delete(self, session: AsyncSession, user_id: int):
        await session.execute(delete(UserModel).where(UserModel.user_id == user_id))
        await session.commit()

    @with_session
    async def create(self, session: AsyncSession, user_id: int, fullname: str, username: str):
        await self.delete(user_id=user_id)
        session.add(UserModel(
            user_id=user_id,
            fullname=fullname,
            username=username,
            status='started'
        ))
        await session.commit()

    @with_session
    async def add(self, session: AsyncSession, user_id: int, user_login: str, user_password: str, fullname: str, username: str):
        user = UserModel(
            user_id=user_id,
            login=user_login,
            fullname=fullname,
            username=username,
            password=user_password,
            status='registered'
        )
        await session.merge(user)
        await session.commit()

    @with_session
    async def update_activity(self, session: AsyncSession, user_id: int):
        result = await session.execute(select(UserModel).where(UserModel.user_id == user_id).with_for_update())
        user = result.scalar_one_or_none()

        if not user:
            return

        user.updated = func.now()
        await session.commit()

    @with_session
    async def get_login_password(self, session: AsyncSession, user_id: int):
        user = await session.execute(select(UserModel).where(UserModel.user_id == user_id))
        user = user.scalar_one_or_none()
        if not user:
            return None, None
        return user.login, user.password

    @with_session
    async def get_all(self, session: AsyncSession):
        users_id = await session.execute(select(UserModel.user_id))
        return users_id.scalars().all()

    @with_session
    async def set_status(self, session: AsyncSession, user_id: int, status: str):
        await session.execute(update(UserModel).where(UserModel.user_id == user_id).values(status=status))
        await session.commit()

    @with_session
    async def get_status(self, session: AsyncSession, user_id: int):
        result = await session.execute(select(UserModel.status).where(UserModel.user_id == user_id))
        return result.scalar_one_or_none()

