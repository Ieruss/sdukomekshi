from aiogram.fsm.state import StatesGroup, State


class QuestionState(StatesGroup):
    question = State()
    from_message_id = State()
