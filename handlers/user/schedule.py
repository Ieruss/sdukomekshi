from aiogram import Router, types, F
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from database.engine import Database
from structure.filters.chat_types import ChatTypeFilter
from structure.inline.schedule import schedule_inline_keyboard
from utils.formating import get_formated_schedule

router = Router(name='schedule')
router.message.filter(ChatTypeFilter([ChatType.PRIVATE]))


@router.message(Command('schedule'))
async def schedule_handler(message: types.Message, state: FSMContext, db: Database):
    await state.clear()
    user_id = message.from_user.id
    user_schedule = await get_formated_schedule(user_id, db, 0)
    await message.answer(f"<pre>{user_schedule}</pre>", reply_markup=schedule_inline_keyboard(1))


@router.callback_query(F.data.startswith("schedule_part_"))
async def schedule_callback_handler(callback: CallbackQuery, db: Database):
    user_id = callback.from_user.id
    part = int(callback.data.split("_")[2])
    current_part = int(callback.data.split("_")[-1])

    if current_part != part:
        await callback.answer(text="You are already on this part")
    else:
        user_schedule = await get_formated_schedule(user_id, db, part)
        await callback.message.edit_text(f"<pre>{user_schedule}</pre>", reply_markup=schedule_inline_keyboard(int(not part)))
        await callback.answer()

