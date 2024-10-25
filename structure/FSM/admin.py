from aiogram.fsm.state import StatesGroup, State

class NotifyUsersState(StatesGroup):
    notify_text = State()