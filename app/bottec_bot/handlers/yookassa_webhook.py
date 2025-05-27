from fastapi import APIRouter, Request
import logging

router = APIRouter()


@router.post('/yookassa/webhook')
async def yookassa_webhook(request: Request):
    payload = await request.json()
    logging.info(f"ЮKassa webhook: {payload}")

    if payload.get('event') != 'payment.succeeded':
        return {'status': 'ignored'}

    payment = payload.get('object', {})
    tg_id = int(payment.get('metadata', {}).get('tg_id', 0))

    # TODO: Тут можно отметить заказ как оплаченный, уведомить бота и т.д.
    logging.info(f"Payment succeeded from user {tg_id}")

    return {'status': 'ok'}