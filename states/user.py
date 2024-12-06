from aiogram.fsm.state import StatesGroup, State

class Registration(StatesGroup):
    language = State()
    name = State()
    phone = State()
    confirmation = State()
    change_name = State()
    change_phone = State()
