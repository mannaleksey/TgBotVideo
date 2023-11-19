import asyncio
from aiogram import executor
from aiogram.types import BotCommand
from handlers import dp
from handlers.users import purchase
from loader import bot
from src.handlers import fsm
from src.handlers.admin import admin


async def set_default_commands():
    await bot.set_my_commands(
        commands=[
            BotCommand('start', 'Запустить бота'),
        ]
    )


async def main():
    await set_default_commands()

if __name__ == '__main__':
    admin.register_handler_admin()
    purchase.register_handler_client()
    fsm.register_handler_fsm()
    executor.start_polling(dp, skip_updates=True)
    asyncio.run(main())
