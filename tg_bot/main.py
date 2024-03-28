from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import asyncio

from aiogram.fsm.strategy import FSMStrategy

from config import TOKEN
from handlers.user_private import user_private_router


bot = Bot(token=TOKEN)
ALLOW_UPDATES = ["message", "edited_message"]
#fsm_strategy=FSMStrategy.USER_IN_CHAT
dp = Dispatcher()

dp.include_router(user_private_router)

async def main():
	await dp.start_polling(bot, allowed_updates=ALLOW_UPDATES)


asyncio.run(main())