from database.engine import Database
from parsing.grades import parse_grades
from parsing.schedule import parse_schedule


async def calc_user_data(user_id, user_login, user_password, fullname, username, db: Database):
    await db.user.add(user_id, user_login, user_password, fullname, username)
    user_schedule = await parse_schedule(user_login, user_password)
    user_grades = await parse_grades(user_login, user_password)
    await db.schedule.add(user_id=user_id, user_schedule=user_schedule)
    await db.grade.add(user_id=user_id, user_grades=user_grades)
