from functools import wraps
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import UserModel, ScheduleModel
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


class ScheduleClass:
    def __init__(self, session_pool: async_sessionmaker):
        self.session_pool = session_pool

    @with_session
    async def add(self, session: AsyncSession, user_id, user_schedule) -> None:
        user = await session.execute(select(UserModel).where(UserModel.user_id == user_id))
        user = user.scalar_one_or_none()

        if not user:
            return

        existing_schedule = await session.execute(select(ScheduleModel).where(ScheduleModel.user_id == user_id))
        existing_schedule = existing_schedule.scalar_one_or_none()

        if existing_schedule:
            return

        for time, day, lesson, location in user_schedule:
            session.add(ScheduleModel(
                user_id=user_id,
                time=time,
                day=day,
                lesson=lesson,
                location=location
            ))

        await session.commit()

    @with_session
    async def get(self, session: AsyncSession, user_id: int):
        schedule = await session.execute(
            select(ScheduleModel).where(
                ScheduleModel.user_id == user_id,
                ~ScheduleModel.location.ilike('%SH%')
            )
        )
        return schedule.scalars().all()

    @with_session
    async def get_lessons_by_parameters(self, session: AsyncSession, day, hour, minute):
        formatted_time = f'{hour}:{minute}'

        schedule = await session.execute(
            select(ScheduleModel.user_id, ScheduleModel.lesson, ScheduleModel.location).where(
                and_(
                    ScheduleModel.day == day,
                    ScheduleModel.time == formatted_time,
                    ~ScheduleModel.location.ilike('%SH%'),
                    
                )
            )
        )
        return schedule.fetchall()
