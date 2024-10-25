from functools import wraps
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import MessageModel
from sqlalchemy.ext.asyncio import async_sessionmaker


def with_session(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        session = kwargs.get('session', None)
        if session is not None:
            return await func(self, session, *args, **kwargs)
        else:
            async with self.session_pool() as session:
                return await func(self, session, *args, **kwargs)

    return wrapper


class MessageClass:
    def __init__(self, session_pool: async_sessionmaker):
        self.session_pool = session_pool

    @with_session
    async def add(self, session: AsyncSession, user_id: int, from_message_id: int, to_message_id: int, question: str):
        session.add(MessageModel(
            user_id=user_id,
            from_message_id=from_message_id,
            to_message_id=to_message_id,
            question=question,
        ))
        await session.commit()

    @with_session
    async def add_answer(self, session: AsyncSession, message_id: int, answer: str):
        result = await session.execute(select(MessageModel).where(MessageModel.to_message_id == message_id))
        message = result.scalar_one_or_none()

        if not message:
            return

        message.answer = answer
        await session.commit()

    @with_session
    async def get_by_to_message_id(self, session: AsyncSession, to_message_id):
        result = await session.execute(select(MessageModel).where(MessageModel.to_message_id == to_message_id))
        return result.scalar_one_or_none()