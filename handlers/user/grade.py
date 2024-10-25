from aiogram.enums import ChatType
from aiogram.fsm.context import FSMContext
from database.engine import Database
from aiogram import Router, types
from aiogram.filters import Command
from structure.filters.chat_types import ChatTypeFilter
from utils.formating import get_formated_grade

router = Router(name='grade')
router.message.filter(ChatTypeFilter([ChatType.PRIVATE]))


@router.message(Command('grade'))
async def grade_handler(message: types.Message, state: FSMContext, db: Database):
    await state.clear()
    user_id = message.from_user.id
    user_grades = await get_formated_grade(user_id, db)
    await message.answer(f"<pre>{user_grades}</pre>")