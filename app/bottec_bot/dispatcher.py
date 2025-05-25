from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from app.bottec_bot.config import config
from app.bottec_bot.handlers.user import start

bot = Bot(
    token=config.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode='HTML')
)
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(start.router)