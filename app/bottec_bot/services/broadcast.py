from asgiref.sync import async_to_sync, sync_to_async
from app.bottec_bot.dispatcher import bot
from app.admin.catalog_admin.models import Broadcast, User
from app.bottec_bot.logging.setup import loggers

logger = loggers['bot']


async def send_broadcast_async(broadcast_id: int):
    broadcast = await sync_to_async(Broadcast.objects.get)(id=broadcast_id)
    users = await sync_to_async(list)(User.objects.all())

    for user in users:
        try:
            await bot.send_message(chat_id=user.id, text=broadcast.message)
        except Exception as e:
            logger.info(f'Error sending to {user.id}: {e}')


def send_broadcast_message(broadcast_id: int):
    async_to_sync(send_broadcast_async)(broadcast_id)
