from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from kbds import reply
from aiogram.enums import ParseMode
from fsm_state_class import *
import json

user_private_router = Router()
########################################################################################################################

# NAME
@user_private_router.message(StateFilter(User_stage.phone_num), Command("name"))
async def get_name00(message: types.Message, state: FSMContext):

	await message.reply("Надішліть ваше ім'я ще раз:")
	await state.set_state(User_stage.name)

# PHONE
@user_private_router.message(StateFilter(User_stage.user_location), Command("phone"))
async def get_phone00(message: types.Message, state: FSMContext):

	await message.reply("Надішліть ваш номер ще раз:", reply_markup=reply.phone_kb, parse_mode=ParseMode.HTML)

	await state.set_state(User_stage.phone_num)

# LOCATION

@user_private_router.message(StateFilter(User_stage.problem_description), Command("location"))
async def get_location00(message: types.Message, state: FSMContext):

	await message.reply("Надішліть вашу локацію ще раз:", reply_markup=reply.location_kb, parse_mode=ParseMode.HTML)

	await state.set_state(User_stage.user_location)

# DESCRIPTION
@user_private_router.message(StateFilter(User_stage.ready_send), Command("description"))
async def get_description00(message: types.Message, state: FSMContext):

	await message.reply("Надішліть вашу проблему ще раз:", reply_markup=types.ReplyKeyboardRemove(), parse_mode=ParseMode.HTML)

	await state.set_state(User_stage.problem_description)


########################################################################################################################

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
		await state.update_data(location=str(message.location))

	elif message.text:
		await state.update_data(location=str(message.text))

	else:
		await message.reply("<b>Шось пішло не так, спробуйте ще раз!</b>", parse_mode=ParseMode.HTML)

	await state.set_state(User_stage.problem_description)
	await message.reply("<b>Локацію успішно збережено!</b>", reply_markup=types.ReplyKeyboardRemove(), parse_mode=ParseMode.HTML)

	await message.answer("Опишіть вашу проблему (-) пропустити:")


# DESCRIPTION
@user_private_router.message(StateFilter(User_stage.problem_description), F.text)
async def get_description(message: types.Message, state: FSMContext):


	if message.text:
		await state.update_data(problem_description=message.text)

		user_data = await state.get_data()
		final_json = json.dumps(user_data)
		pretty_user_data = "\n".join(f"<b>{key}:</b> {value}" for key, value in user_data.items())

		final_json = json.dumps(user_data)

		await message.answer(f"<b>Ваша заявка:</b>\n{pretty_user_data}", parse_mode=ParseMode.HTML)
		await message.answer(f"<b>Ваша заява надіслана успішно, очікуйте допомоги</b>", parse_mode=ParseMode.HTML)



	else:
		await message.reply("<b>Шось пішло не так, спробуйте ще раз!</b>", parse_mode=ParseMode.HTML)

	await state.clear()


# SEND DATA
# @user_private_router.message(StateFilter(User_stage.ready_send), F.text)
# async def get_send(message: types.Message, state: FSMContext):
#
# 	user_data = await state.get_data()
# 	final_json = json.dumps(user_data)
# 	pretty_user_data = "\n".join(f"<b>{key}:</b> {value}" for key, value in user_data.items())
#
# 	final_json = json.dumps(user_data)
#
# 	await message.answer(f"<b>Ваша заявка:</b>\n{pretty_user_data}", parse_mode=ParseMode.HTML)


# if message.text == "Так":
	# 	# user_data = await state.get_data()
	# 	# final_json = json.loads(str(user_data).replace("'", '"'))
	#
	# 	# відправка на сервер
	# 	# відправка на сервер
	# 	# відправка на сервер
	#
	# 	await message.answer("<b>Ваша заявка надіслана успішно очікуйте допомоги</b>", parse_mode=ParseMode.HTML, reply_markup=types.ReplyKeyboardRemove())
	# elif message.text == "Ні":
	# 	await message.answer("<b>Виберіть потрібний пункт для зміни в меню зліва</b>", parse_mode=ParseMode.HTML, reply_markup=types.ReplyKeyboardRemove())
	#

########################################################################################################################



# NAME
@user_private_router.message(StateFilter(User_stage.user_location), Command("name"))
async def get_name99(message: types.Message, state: FSMContext):
	await message.reply("Надішліть ваше ім'я ще раз:")
	await state.set_state(User_stage.name)


@user_private_router.message(StateFilter(User_stage.problem_description), Command("name"))
async def get_name88(message: types.Message, state: FSMContext):
	await message.reply("Надішліть ваше ім'я ще раз:")
	await state.set_state(User_stage.name)


@user_private_router.message(StateFilter(User_stage.ready_send), Command("name"))
async def get_name77(message: types.Message, state: FSMContext):
	await message.reply("Надішліть ваше ім'я ще раз:")
	await state.set_state(User_stage.name)



# PHONE
@user_private_router.message(StateFilter(User_stage.user_location), Command("phone"))
async def get_phone66(message: types.Message, state: FSMContext):
	await message.reply("Надішліть ваш номер ще раз:", reply_markup=reply.phone_kb, parse_mode=ParseMode.HTML)

	await state.set_state(User_stage.phone_num)


@user_private_router.message(StateFilter(User_stage.problem_description), Command("phone"))
async def get_phone55(message: types.Message, state: FSMContext):
	await message.reply("Надішліть ваш номер ще раз:", reply_markup=reply.phone_kb, parse_mode=ParseMode.HTML)

	await state.set_state(User_stage.phone_num)


@user_private_router.message(StateFilter(User_stage.ready_send), Command("phone"))
async def get_phone44(message: types.Message, state: FSMContext):
	await message.reply("Надішліть ваш номер ще раз:", reply_markup=reply.phone_kb, parse_mode=ParseMode.HTML)

	await state.set_state(User_stage.phone_num)




# LOCATION

@user_private_router.message(StateFilter(User_stage.problem_description), Command("location"))
async def get_location33(message: types.Message, state: FSMContext):
	await message.reply("Надішліть вашу локацію ще раз:", reply_markup=reply.location_kb, parse_mode=ParseMode.HTML)

	await state.set_state(User_stage.user_location)


@user_private_router.message(StateFilter(User_stage.problem_description), Command("location"))
async def get_location22(message: types.Message, state: FSMContext):
	await message.reply("Надішліть вашу локацію ще раз:", reply_markup=reply.location_kb, parse_mode=ParseMode.HTML)

	await state.set_state(User_stage.user_location)


@user_private_router.message(StateFilter(User_stage.ready_send), Command("location"))
async def get_location11(message: types.Message, state: FSMContext):
	await message.reply("Надішліть вашу локацію ще раз:", reply_markup=reply.location_kb, parse_mode=ParseMode.HTML)

	await state.set_state(User_stage.user_location)



# # DESCRIPTION
# @user_private_router.message(StateFilter(User_stage.ready_send), Command("description"))
# async def get_description(message: types.Message, state: FSMContext):
# 	await message.reply("Надішліть вашу проблему ще раз:", reply_markup=types.ReplyKeyboardRemove(), parse_mode=ParseMode.HTML)
#
# 	await state.set_state(User_stage.problem_description)
