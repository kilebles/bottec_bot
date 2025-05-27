from fastapi import APIRouter, Request
from aiogram.types import Update
import logging

from app.bottec_bot.dispatcher import bot, dp

router = APIRouter()


@router.post('/webhook')
async def telegram_webhook(request: Request):
    try:
        body = await request.json()
        update = Update.model_validate(body)
        await dp.feed_update(bot, update)
        return {'ok': True}
    except Exception as e:
        logging.error(f'Error in webhook: {e}')
        return {'ok': False}
