import asyncio
import os

from database.query.grade import GradeClass
from database.query.message import MessageClass
from database.query.schedule import ScheduleClass
from database.query.user import UserClass
from database.query.user_statistics import UserStatisticsClass
from utils.config import load_config
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from database.models import Base


class Database:
    def __init__(self):
        self.config = load_config()
        self.engine = create_async_engine(url=self.config.db.dsn(), echo=self.config.db.IS_ECHO)
        self.session_maker = async_sessionmaker(bind=self.engine, class_=AsyncSession, expire_on_commit=False)
        self.schedule = ScheduleClass(self.session_maker)
        self.user = UserClass(self.session_maker)
        self.grade = GradeClass(self.session_maker)
        self.user_statistics = UserStatisticsClass(self.session_maker)
        self.message = MessageClass(self.session_maker)

    async def create_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


if __name__ == "__main__":
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(Database().create_db())
