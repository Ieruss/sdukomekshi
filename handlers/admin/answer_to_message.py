from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from database.engine import Database
from loader import bot
from structure.filters.admin import AdminFilter
from structure.filters.chat_id import ChatIDFilter
from structure.filters.chat_types import ChatTypeFilter
from structure.inline.confirm import qa_confirm_keyword

router = Router(name='statistics')
router.message.filter(ChatTypeFilter([ChatType.GROUP, ChatType.SUPERGROUP]))


@router.message(AdminFilter(), ChatIDFilter())
async def answer_handler(message: Message, state: FSMContext):
    await state.clear()
    if not message.reply_to_message:
        return
    text = message.text
    await state.update_data(question_id=message.reply_to_message.message_id)
    await message.answer(text, reply_to_message_id=message.message_id, reply_markup=qa_confirm_keyword)


@router.callback_query(F.data == 'qa_send', AdminFilter(), ChatIDFilter())
async def send_confirm(callback, state: FSMContext, db: Database):
    answer = callback.message.text
    question_id = (await state.get_data()).get('question_id')
    msg_data = await db.message.get_by_to_message_id(question_id)
    await db.message.add_answer(message_id=question_id, answer=answer)
    msg = f"<b>Admin</b>\n\n{answer}"

    try:
        await bot.send_message(chat_id=msg_data.user_id, text=msg, reply_to_message_id=msg_data.from_message_id)
    except:
        await bot.send_message(chat_id=msg_data.user_id, text=msg)

    await callback.message.edit_text("Sent ✅")


@router.callback_query(F.data == 'qa_cancel', AdminFilter(), ChatIDFilter())
async def send_cancel(callback, state: FSMContext):
    await callback.message.edit_text("Cancelled ❌")
    await state.clear()
