import asyncio

from app.bottec_bot.dispatcher import bot
from app.bottec_bot.db.models import User
from app.admin.catalog_admin.models import Broadcast


async def send_broadcast_async(broadcast_id: int):
    broadcast = Broadcast.objects.get(id=broadcast_id)
    users = User.objects.all()

    for user in users:
        try:
            await bot.send_message(chat_id=user.id, text=broadcast.message)
        except Exception as e:
            print(f'Error sending to {user.id}: {e}')


def send_broadcast_message(broadcast_id: int):
    asyncio.run(send_broadcast_async(broadcast_id))
