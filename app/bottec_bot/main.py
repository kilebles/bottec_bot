import logging

from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.bottec_bot.dispatcher import bot
from app.bottec_bot.config import config
from app.bottec_bot.UI.commands import set_default_commands
from app.bottec_bot.handlers.yookassa_webhook import router as yookassa_router
from app.bottec_bot.handlers.telegram_webhook import router as telegram_router
from app.bottec_bot.logging.setup import loggers

logger = loggers['bot']


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info('Setting webhook...')
    await bot.set_webhook(config.WEBHOOK_URL)
    logger.debug(f'Webhook set to: {config.WEBHOOK_URL}')
    await set_default_commands(bot)
    yield
    logging.info('Shutting down...')
    await bot.delete_webhook()
    await bot.session.close()


app = FastAPI(lifespan=lifespan)
app.include_router(telegram_router)
app.include_router(yookassa_router)
