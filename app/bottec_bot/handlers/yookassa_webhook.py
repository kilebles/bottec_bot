import logging

from fastapi import APIRouter, Request

from app.bottec_bot.logging.setup import loggers

logger = loggers['bot']

router = APIRouter()


@router.post('/yookassa/webhook')
async def yookassa_webhook(request: Request):
    try:
        payload = await request.json()
        logger.debug(f'ЮKassa webhook received: {payload}')

        if payload.get('event') != 'payment.succeeded':
            logger.info(f"Ignored event: {payload.get('event')}")
            return {'status': 'ignored'}

        payment = payload.get('object', {})
        tg_id = int(payment.get('metadata', {}).get('tg_id', 0))
        amount = payment.get('amount', {}).get('value', 'N/A')
        
        logger.info(f"Payment succeeded: user={tg_id}, amount={amount}")

        # TODO: Отметить заказ как оплаченный, уведомить бота и т.д.
        logging.info(f"Payment succeeded from user {tg_id}")

        return {'status': 'ok'}
    except Exception as e:
            logger.exception(f'Error in YooKassa webhook: {e}')
            return {'status': 'error'}