from aiogram.fsm.state import StatesGroup, State


class User_stage(StatesGroup):
    # username = State
    init_start = State()
    name = State()
    phone_num = State()
    user_location = State()
    problem_description = State()
    ready_send = State()