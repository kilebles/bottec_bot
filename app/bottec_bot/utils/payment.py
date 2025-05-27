import json
import uuid
import logging
import os
from yookassa import Configuration, Payment

from app.bottec_bot.config import config

Configuration.account_id = config.YOOKASSA_ID
Configuration.secret_key = config.YOOKASSA_KEY


async def create_yoomoney_payment(value: str, description: str, tg_id: int) -> dict:
    try:
        idempotence_key = str(uuid.uuid4())
        payment = Payment.create(
            {
                "amount": {"value": value, "currency": "RUB"},
                "confirmation": {
                    "type": "redirect",
                    "return_url": "https://your-site.ru",
                },
                "capture": True,
                "description": description,
                "metadata": {"tg_id": tg_id},
            },
            idempotence_key,
        )

        return json.loads(payment.json())
    except Exception as e:
        logging.error(f"Ошибка при создании платежа: {e}")
        raise