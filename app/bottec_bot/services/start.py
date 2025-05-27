from aiogram.types import User as TelegramUser
from sqlalchemy import select

from app.bottec_bot.db.repo import get_session
from app.bottec_bot.db.models import TelegramResource, User


async def get_or_create_user(tg_user: TelegramUser) -> User:
    async with get_session() as session:
        user = await session.get(User, tg_user.id)
        if user is None:
            user = User(
                id=tg_user.id,
                username=tg_user.username,
            )
            session.add(user)
        return user


async def get_required_resources() -> list[TelegramResource]:
    async with get_session() as session:
        stmt = select(TelegramResource)
        result = await session.execute(stmt)
        return result.scalars().all()
