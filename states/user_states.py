from aiogram.fsm.state import StatesGroup, State


class RequestInfo(StatesGroup):
    name = State()
    surname = State()
    age = State()