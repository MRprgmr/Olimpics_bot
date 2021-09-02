from aiogram.dispatcher.filters.state import StatesGroup, State


class Registration(StatesGroup):
    full_name = State()
    grade = State()
    phone_number = State()
    is_poorly_supplied = State()
    confirmation = State()
