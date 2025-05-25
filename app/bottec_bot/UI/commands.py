from aiogram import Bot
from aiogram.types import BotCommand


async def set_default_commands(bot: Bot):
    commands = [
        BotCommand(command='start', description='🚀 Запуск')
    ]
    
    await bot.set_my_commands(commands)