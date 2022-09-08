from aiogram.dispatcher.filters.state import StatesGroup, State


class StatesChange(StatesGroup):
    STATE_EMPTY = State()
    STATE_VALUE = State()
    STATE_SPREAD = State()
    STATE_MIN_GOOD = State()
    STATE_MAX_BAD = State()