from aiogram import Router, types
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from database.engine import Database
from structure.filters.chat_types import ChatTypeFilter
from utils.formating import get_formated_attendance

router = Router(name="attendance")
router.message.filter(ChatTypeFilter([ChatType.PRIVATE]))


@router.message(Command('attendance'))
async def grade_handler(message: types.Message, state: FSMContext, db: Database):
    await state.clear()
    user_id = message.from_user.id
    user_grades = await get_formated_attendance(user_id, db)
    await message.answer(f"<pre>{user_grades}</pre>")
