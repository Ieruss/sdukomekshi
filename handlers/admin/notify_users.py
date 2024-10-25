from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from arq import ArqRedis
from structure.FSM.admin import NotifyUsersState
from structure.filters.admin import AdminFilter
from structure.filters.chat_types import ChatTypeFilter
from structure.inline.confirm import confirm_keyword

router = Router(name='notify_users')
router.message.filter(ChatTypeFilter([ChatType.PRIVATE]))


@router.message(Command('send_all'), AdminFilter())
async def send_all_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Enter the <b>message</b>:")
    await state.set_state(NotifyUsersState.notify_text)


@router.message(NotifyUsersState.notify_text, AdminFilter())
async def notify_text_handler(message: Message, state: FSMContext):
    notify_text = message.text
    await state.update_data(notify_text=notify_text)
    await message.answer(notify_text, reply_markup=confirm_keyword, reply_to_message_id=message.message_id)


@router.callback_query(F.data == 'send', AdminFilter())
async def send_all_confirm(callback: CallbackQuery, state: FSMContext, arqredis: ArqRedis):
    notify_text = (await state.get_data()).get('notify_text')
    main_msg = await callback.message.edit_text("sending...")
    clb_msg = await callback.message.answer('0%')
    await arqredis.enqueue_job('notify_all_users', msg_id=clb_msg.message_id, main_msg_id = main_msg.message_id, text=notify_text)
    await state.clear()


@router.callback_query(F.data == 'cancel', AdminFilter())
async def send_all_cancel(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Cancelled")
    await state.clear()
