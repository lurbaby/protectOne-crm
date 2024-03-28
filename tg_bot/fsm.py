from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import asyncio

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.strategy import FSMStrategy

from config import TOKEN
from handlers.user_private import user_private_router



class User_stage(StatesGroup):
    init_start = State()
    name = State()
    phone_num = State()
    user_location = State()
    problem_description = State()