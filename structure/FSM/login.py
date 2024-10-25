from aiogram.fsm.state import StatesGroup, State

class LoginState(StatesGroup):
    login = State()
    password = State()

