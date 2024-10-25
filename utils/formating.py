import asyncio
import sys
from collections import defaultdict

from structure.constant.grade import get_gpa

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from tabulate import tabulate
from structure.constant.template import time_slots
from database.engine import Database
from parsing.grades import parse_grades


async def get_formated_grade(user_id, db: Database):
    username, password = await db.user.get_login_password(user_id)
    arr = await parse_grades(username, password)
    need_arr = [[row[0], row[2], row[3], get_gpa(row[2])] for row in arr]
    headers = ["Subject", "Score", "Grade", "GPA"]
    table_string = tabulate(need_arr, headers, tablefmt="simple", colalign=("left",) * len(headers))
    await db.grade.update(user_id, need_arr)
    return table_string


async def get_formated_attendance(user_id, db: Database):
    username, password = await db.user.get_login_password(user_id)
    arr = await parse_grades(username, password)
    need_arr = [[row[0], row[1]+"%"] for row in arr]
    headers = ["Subject", "Attendance"]
    table_string = tabulate(need_arr, headers, tablefmt="simple", colalign=("left",) * len(headers))
    await db.grade.update(user_id, arr)
    return table_string


async def get_formated_schedule(user_id, db, part=0):
    schedules = await db.schedule.get(user_id)

    days = ["MO", "TU", "WE"]
    if part == 1:
        days = ['TH', 'FR', 'SA']

    schedule_table = defaultdict(lambda: {day: "" for day in days})

    for schedule in schedules:
        day_abbreviation = schedule.day[:2].upper()
        if day_abbreviation in days:
            schedule_table[schedule.time][day_abbreviation] = f"{schedule.lesson}\n{schedule.location}"

    headers = ["T/D"] + days
    table_data = []

    for time_slot in time_slots:
        row = [time_slot[0] + "\n" + time_slot[1]] + [schedule_table[time_slot[0]][day] for day in days]
        table_data.append(row)

    table_string = tabulate(table_data, headers, tablefmt="grid", colalign=("center", "center", "center", "center"))
    return table_string


async def main():
    from loader import db
    e = await get_formated_schedule(747117107, db, 1)
    print(e)


if __name__ == '__main__':
    asyncio.run(main())
