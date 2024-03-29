from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

phone_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Ваш номер', request_contact=True),
        ],
    ],
    resize_keyboard=True,
)
location_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Ваша локація', request_location=True),
        ],
    ],
    resize_keyboard=True,
)

ready_data = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Так'),
            KeyboardButton(text='Ні'),
        ],
    ],
    resize_keyboard=True,
)