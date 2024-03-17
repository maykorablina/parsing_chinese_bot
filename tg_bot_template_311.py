import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

TOKEN_API = "token"
bot = Bot(TOKEN_API, parse_mode="HTML")
dp = Dispatcher()


@dp.message(Command("start"))
async def beginning(message):
    pass



async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
