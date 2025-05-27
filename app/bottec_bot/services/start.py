from bottec_bot.db.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from admin.catalog_admin.models import TelegramResource


async def get_or_create_user(session: AsyncSession, tg_user: TelegramUser) -> User:
    user = await session.get(User, tg_user.id)
    if user is None:
        user = User(
            id=tg_user.id,
            username=tg_user.username,
        )
        session.add(user)
    return user


async def get_required_resources(session: AsyncSession) -> list[TelegramResource]:
    stmt = select(TelegramResource)
    result = await session.execute(stmt)
    return result.scalars().all()