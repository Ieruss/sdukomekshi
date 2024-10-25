import os
import sys
import asyncio
from arq import cron
from aiogram import Bot
from loader import config
from scheduler.cron.attendance import periodic_attendance_check
from scheduler.cron.lesson import notify_lesson
from scheduler.sender import send_message
from arq.connections import RedisSettings
from scheduler.notify_users import notify_all_users

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

async def startup(ctx):
    ctx['bot'] = Bot(token=config.tg_bot.token)

async def shutdown(ctx):
    await ctx['bot'].session.close()

class WorkerSettings:
    redis_settings = RedisSettings(host='localhost', port=6380)
    on_startup = startup
    on_shutdown = shutdown
    functions = [send_message, notify_all_users]

    cron_jobs = [
        cron(notify_lesson, minute=10),
        cron(periodic_attendance_check, minute={0, 10, 20, 30, 40, 50})
    ]
