from aiogram import Router

from handlers.user.start import router as user_start_router
from handlers.user.schedule import router as user_schedule_router
from handlers.user.grade import router as user_grade_router
from handlers.user.attendance import router as user_attendance_router
from handlers.admin.notify_users import router as admin_notify_users_router
from handlers.admin.statistics import router as admin_statistics_router
from handlers.user.message import router as user_message_router
from handlers.admin.answer_to_message import router as admin_answer_to_message_router

def setup_routers() -> Router:
    router = Router()
    router.include_routers(user_start_router,
                           user_grade_router,
                           user_attendance_router,
                           user_schedule_router,
                           user_message_router,
                           admin_notify_users_router,
                           admin_statistics_router,
                           admin_answer_to_message_router
                           )
    return router
