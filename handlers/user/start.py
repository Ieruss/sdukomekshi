from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.engine import Database
from parsing.initial import calc_user_data
from structure.constant.checker import check_user_login, check_user
from structure.filters.chat_types import ChatTypeFilter
from structure.inline.login import login_keyword, rewrite_login_keyword
from structure.FSM.login import LoginState
from utils.set_bot_commands import set_start_commands

router = Router(name='start',)
router.message.filter(ChatTypeFilter([ChatType.PRIVATE]))

@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext, db: Database):
    await state.clear()
    await db.user.create(user_id=message.from_user.id, fullname=message.from_user.full_name, username=message.from_user.username)
    await set_start_commands(user_id = message.from_user.id)
    await message.answer(
        "<b>👋 Welcome!</b>\n\n"
        "🎓 This bot helps students by providing quick access to important information, such as <b>student passes</b>.\n\n"
        "🚀 To get started, just click the <b>Login</b> button below.",
        parse_mode="HTML",
        reply_markup=login_keyword
    )



@router.callback_query(F.data == 'login')
async def introduction(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("👤 **Enter your login**: `240110105`", parse_mode="Markdown")
    await state.set_state(LoginState.login)


@router.message(LoginState.login)
async def login(message: Message, state: FSMContext):
    user_login = message.text
    if not check_user_login(user_login):
        await message.answer("❌ Invalid login, try again", reply_markup=rewrite_login_keyword)
        return
    await state.update_data(login=user_login)
    await state.set_state(LoginState.password)
    await message.answer("🔑 **Enter your password**", parse_mode="Markdown")


@router.callback_query(F.data == 'rewrite_login')
async def rewrite_login(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("👤 **Enter your login**: `240110105`", parse_mode="Markdown")
    await state.set_state(LoginState.login)


@router.message(LoginState.password)
async def password(message: Message, state: FSMContext, db: Database):
    msg = await message.answer("Logging in...")
    user_id = message.from_user.id
    user_login = (await state.get_data()).get('login')
    user_password = message.text
    if not await check_user(user_login, user_password):
        await msg.edit_text("❌ **Incorrect username or password, try again**", reply_markup=rewrite_login_keyword, parse_mode="Markdown")
        return

    await state.clear()
    username = message.from_user.username
    fullname = message.from_user.full_name
    await calc_user_data(user_id, user_login, user_password, fullname, username, db)
    await msg.edit_text("✅ You have successfully logged in!")
