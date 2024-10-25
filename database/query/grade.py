from asyncio.log import logger
from functools import wraps
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import UserModel, GradeModel
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


class GradeClass:
    def __init__(self, session_pool: async_sessionmaker):
        self.session_pool = session_pool

    @with_session
    async def add(self, session: AsyncSession, user_id, user_grades) -> None:
        user = await session.execute(select(UserModel).where(UserModel.user_id == user_id))
        user = user.scalar_one_or_none()

        if not user:
            logger.info(f"{user_id} User not found")
            return

        for lesson, absense, grade, letter_grade in user_grades:
            session.add(GradeModel(
                user_id=user_id,
                lesson=lesson,
                absence=absense,
                grade=grade,
                letter_grade=letter_grade
            ))

        await session.commit()

    @with_session
    async def update(self, session: AsyncSession, user_id, user_grades) -> None:
        for lesson, absense, grade, letter_grade in user_grades:
            existing_grade = await session.execute(
                select(GradeModel).where(
                    GradeModel.user_id == user_id,
                    GradeModel.lesson == lesson
                )
            )
            existing_grade = existing_grade.scalar_one_or_none()

            if existing_grade:
                existing_grade.absence = absense
                existing_grade.grade = grade
                existing_grade.letter_grade = letter_grade
            else:
                session.add(GradeModel(
                    user_id=user_id,
                    lesson=lesson,
                    absence=absense,
                    grade=grade,
                    letter_grade=letter_grade
                ))

        await session.commit()

    @with_session
    async def get_attendance(self, session: AsyncSession, user_id):
        attendance = await session.execute(
            select(GradeModel.lesson, GradeModel.absence).where(
                GradeModel.user_id == user_id
            )
        )
        return attendance.fetchall()
