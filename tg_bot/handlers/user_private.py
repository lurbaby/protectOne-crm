import json

from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from kbds import reply
from aiogram.enums import ParseMode
from fsm_state_class import *


user_private_router = Router()

# START
@user_private_router.message(StateFilter(None), CommandStart())
async def start_msg(message: types.Message, state: FSMContext):

	await message.reply("<b>Доброго дня, я бот швидкого реагування</b>\nдля того щоб продовжити введіть ваш <b><i>ПІБ</i></b>", parse_mode=ParseMode.HTML)

	await state.update_data(username=message.from_user.username)

	await state.set_state(User_stage.name)

# NAME
@user_private_router.message(StateFilter(User_stage.name), F.text)
async def get_name(message: types.Message, state: FSMContext):

	if message.text and message.text[0].isalpha():
		await state.update_data(name=message.text)


		await message.reply("<b>ПІБ успішно збережено!</b>", parse_mode=ParseMode.HTML)
		await message.answer("Надішліть ваш номер телефону:", reply_markup=reply.phone_kb)
		await state.set_state(User_stage.phone_num)
	else:
		await message.reply("<b>Шось пішло не так, спробуйте ще раз!</b>", parse_mode=ParseMode.HTML)

# PHONE
@user_private_router.message(StateFilter(User_stage.phone_num), F.contact | F.text)
async def get_phone(message: types.Message, state: FSMContext):

	phone_number = ""
	if message.text or message.contact.phone_number:

		if message.contact and message.contact.phone_number:
			if (str(message.contact.phone_number)[0].isdigit() and str(message.contact.phone_number).startswith("380")):
				phone_number = "+" + str(message.contact.phone_number)

			elif str(message.contact.phone_number).startswith("+380"):
				phone_number = str(message.contact.phone_number)

			else:
				phone_number = str(message.contact.phone_number)


		elif message.text:
			if (message.text[0].isdigit() and message.text.startswith("380")):
				phone_number = phone_number = "+" + message.text

			elif message.text.startswith("+380"):
				phone_number = message.text

			else:
				phone_number = message.text


		await state.update_data(phone_num=phone_number)


		await message.reply("<b>Номер успішно збережено!</b>", reply_markup=types.ReplyKeyboardRemove(), parse_mode=ParseMode.HTML)

		await message.answer("Надішліть вашу локацію:", reply_markup=reply.location_kb)
		await state.set_state(User_stage.user_location)
	else:
		await message.reply("<b>Шось пішло не так, спробуйте ще раз!</b>", parse_mode=ParseMode.HTML)



# LOCATION

@user_private_router.message(StateFilter(User_stage.user_location), F.location | F.text)
async def get_location(message: types.Message, state: FSMContext):

	if message.location:
		await state.update_data(location=message.location)

	elif message.text:
		await state.update_data(location=message.text)

	else:
		await message.reply("<b>Шось пішло не так, спробуйте ще раз!</b>", parse_mode=ParseMode.HTML)

	await state.set_state(User_stage.problem_description)
	await message.reply("<b>Локацію успішно збережено!</b>", reply_markup=types.ReplyKeyboardRemove(), parse_mode=ParseMode.HTML)

	await message.answer("Опишіть вашу проблему (-) пропустити:")


# DESCRIPTION
@user_private_router.message(StateFilter(User_stage.problem_description)
@user_private_router.message(StateFilter(User_stage.problem_description), F.text)
async def get_description(message: types.Message, state: FSMContext):


	if message.text:
		await state.update_data(problem_description=message.text)

		user_data = await state.get_data()
		final_json = json.loads(str(user_data).replace("'", '"'))
		await message.answer(f"<b>Ваша заявка:</b>\n{final_json}", parse_mode=ParseMode.HTML)

		await message.answer("<b>Все вірно?</b>", reply_markup=reply.ready_data, parse_mode=ParseMode.HTML)

		await state.set_state(User_stage.ready_send)


	else:
		await message.reply("<b>Шось пішло не так, спробуйте ще раз!</b>", parse_mode=ParseMode.HTML)

# SEND DATA
@user_private_router.message(StateFilter(User_stage.ready_send), F.text)
async def get_description(message: types.Message, state: FSMContext):
	if message.text == "Так":
		user_data = await state.get_data()
		final_json = json.loads(str(user_data).replace("'", '"'))

		# відправка на сервер
		# відправка на сервер
		# відправка на сервер

		await message.answer("<b>Ваша заявка надіслана успішно очікуйте допомоги</b>", parse_mode=ParseMode.HTML, reply_markup=types.ReplyKeyboardRemove())
	elif message.text == "Ні":
		await message.answer("<b>Виберіть потрібний пункт для зміни в меню зліва</b>", parse_mode=ParseMode.HTML, reply_markup=types.ReplyKeyboardRemove())

	await state.clear()


# (щоб виправити натисність в меню на потрібний пункт)



@user_private_router.message(Command("name"))
async def change_name_state(message: types.Message, state: FSMContext):

	await message.answer("Ось ваші данні:")
	# need to write...

@user_private_router.message(Command("phone"))
async def change_phone_state(message: types.Message, state: FSMContext):
	await message.answer("Введіть ваш ПІБ:")
	# need to write...

@user_private_router.message(Command("location"))
async def change_location_state(message: types.Message, state: FSMContext):

	await message.answer("Ось ваші данні:")
	# need to write...

@user_private_router.message(Command("description"))
async def change_description_state(message: types.Message, state: FSMContext):
	await message.answer("Введіть ваш ПІБ:")
	# need to write...

@user_private_router.message(Command("send"))
async def change__state(message: types.Message, state: FSMContext):
	await message.answer("Введіть ваш ПІБ:")
	# need to write...


