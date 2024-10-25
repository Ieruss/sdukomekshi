import asyncio
import sys
from datetime import timedelta, datetime, timezone
from scheduler.sender import send_message
from loader import db, bot

def clarify_hour(hour):
    return f"0{hour}" if hour < 10 else str(hour)


def get_day_of_week(day: int) -> str:
    arr = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    return arr[day] if 0 <= day < 7 else 'None'


async def notify_lesson(ctx):
    today = datetime.now(timezone(timedelta(hours=5)))
    day, hour, minute, = get_day_of_week(today.weekday()), clarify_hour(today.hour), '30'

    datas = await db.schedule.get_lessons_by_parameters(day, hour, minute)
    for user_id, lesson, location in datas:
        msg = f"next lesson: <b>{lesson}</b>, <b>{location}</b>"
        await send_message(ctx, user_id=user_id, text=msg)
        await asyncio.sleep(0.2)

# if __name__ == '__main__':
#     if sys.platform == 'win32':
#         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#
#     ctx = {
#         'bot': bot,
#     }
#     asyncio.run(notify_lesson(ctx=ctx))
