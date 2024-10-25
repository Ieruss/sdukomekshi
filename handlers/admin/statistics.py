from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.engine import Database
from structure.filters.admin import AdminFilter
from structure.filters.chat_types import ChatTypeFilter

router = Router(name='statistics')
router.message.filter(ChatTypeFilter([ChatType.PRIVATE]))


@router.message(Command('statistics'), AdminFilter())
async def statistics_handler(message: Message, state: FSMContext, db: Database):
    await state.clear()
    datas = await db.user_statistics.calc()

    result = '📊 **Bot Statistics**\n\n'

    result += f"👥 **Total Users**: `{datas['total_users']}`\n"
    result += f"✅ **Registered Users**: `{datas['registered_users']}`\n"
    result += f"🚫 **Banned Users**: `{datas['banned_users']}`\n"
    result += f"❌ **Users Without Login**: `{datas['unlogged_users']}`\n\n"

    result += "🕒 **Active Users**\n"
    result += f"   - Last Hour: `{datas['active_last_hour']}`\n"
    result += f"   - Last 6 Hours: `{datas['active_last_6_hours']}`\n"
    result += f"   - Last Day: `{datas['active_last_day']}`\n"
    result += f"   - Last Week: `{datas['active_last_week']}`\n"

    await message.answer(result, parse_mode="Markdown")
