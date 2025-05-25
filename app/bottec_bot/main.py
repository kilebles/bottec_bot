import logging

from fastapi import FastAPI, Request
from aiogram.types import Update
from contextlib import asynccontextmanager

from app.bottec_bot.dispatcher import bot, dp
from app.bottec_bot.config import config
from app.bottec_bot.UI.commands import set_default_commands

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info('Setting webhook...')
    await bot.set_webhook(config.WEBHOOK_URL)
    await set_default_commands(bot)
    yield
    logging.info('Shutting down...')
    await bot.delete_webhook()
    await bot.session.close()


app = FastAPI(lifespan=lifespan)


@app.post('/webhook')
async def telegram_webhook(request: Request):
    try:
        body = await request.json()
        logging.info(f'Incoming Telegram update: {body}')
        update = Update.model_validate(body)
        await dp.feed_update(bot, update)
        return {'ok': True}
    except Exception as e:
        logging.error(f'Error in webhook: {e}')
        return {'ok': False}
