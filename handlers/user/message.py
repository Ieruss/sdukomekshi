from aiogram.enums import ChatType
from aiogram.fsm.context import FSMContext
from aiogram import Router, types, F
from aiogram.filters import Command
from database.engine import Database
from structure.FSM.question import QuestionState
from structure.filters.chat_types import ChatTypeFilter
from structure.inline.confirm import question_confirm_keyword
from loader import config, bot

router = Router(name='question')
router.message.filter(ChatTypeFilter([ChatType.PRIVATE]))


@router.message(Command('message'))
async def question_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Write your <b>question</b>")
    await state.set_state(QuestionState.question)


@router.message(QuestionState.question)
async def ask_question_handler(message: types.Message, state: FSMContext):
    question = message.text
    await state.update_data(question=question)
    await state.update_data(from_message_id=message.message_id)
    await message.answer(text=question, reply_markup=question_confirm_keyword, reply_to_message_id=message.message_id)


@router.callback_query(F.data == 'q_send', QuestionState.question)
async def send_question_handler(callback: types.CallbackQuery, state: FSMContext, db: Database):
    question = (await state.get_data()).get('question')

    from_message_id = (await state.get_data()).get('from_message_id')
    await callback.message.edit_text("Message sent ✅")

    send_question = (f"username: {callback.from_user.full_name}\n"
                     f"mention: @{callback.from_user.username}\n\n"
                     f"{question}")

    to_message_id = await bot.send_message(chat_id=config.chats.QA_CHAT_ID, text=send_question)
    await db.message.add(user_id=callback.from_user.id,
                         from_message_id=from_message_id,
                         to_message_id=to_message_id.message_id,
                         question=question)


@router.callback_query(F.data == 'q_cancel', QuestionState.question)
async def cancel_question_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Message cancelled ❌")
    await state.clear()
