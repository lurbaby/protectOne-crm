from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Ваш номер', request_contact=True),
            KeyboardButton(text='Ваша локація', request_location=True),
        ],
    ],
    resize_keyboard=True,
)

