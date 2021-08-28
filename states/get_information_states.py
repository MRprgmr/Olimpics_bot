from aiogram.dispatcher.filters.state import StatesGroup, State


class OlympiadsState(StatesGroup):
    olympiad = State()
    view = State()
