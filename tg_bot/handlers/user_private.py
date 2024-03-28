from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext

from kbds import reply
from aiogram.enums import ParseMode
from fsm import *

user_private_router = Router()

@user_private_router.message(StateFilter(None), CommandStart())
async def start_msg(message: types.Message, state: FSMContext):
	await message.reply("<b>Доброго дня, я бот швидкого реагування</b>", parse_mode=ParseMode.HTML)
	with open('test.txt', "a") as write_file:
		write_file.write(message.from_user.username + "\n")

	await state.set_state(User_stage.name)


@user_private_router.message(Command("mydata"))
async def your_data(message: types.Message, state: FSMContext):
	await message.answer("Ось ваші данні:")
	# need to write...

@user_private_router.message(Command("pib"))
async def pib_msg(message: types.Message, state: FSMContext):
	await message.answer("Введіть ваш ПІБ:")
	# need to write...


@user_private_router.message(Command("phone"))
async def phone_get_msg(message: types.Message, state: FSMContext):
	await message.answer("Надішліть ваш номер телефону:", reply_markup=reply.start_kb)


@user_private_router.message(F.contact)
async def phone_msg(message: types.Message, state: FSMContext):

	await message.answer(f"Ваш номер отриманий")
	await message.answer(str(message.contact.phone_number))

@user_private_router.message(F.location)
async def phone_msg(message: types.Message, state: FSMContext):

	await message.answer(f"Ваш номер отриманий")
	await message.answer(str(message.location))

