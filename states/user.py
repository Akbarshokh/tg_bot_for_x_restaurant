from aiogram.fsm.state import StatesGroup, State

class Registration(StatesGroup):
    language = State()
    name = State()
    phone = State()
    confirmation = State()

class Settings(StatesGroup):
    change_name = State()
    change_phone = State()

class FeedbackStates(StatesGroup):
    waiting_for_feedback = State()
