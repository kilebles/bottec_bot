from aiogram.types import User as TelegramUser
from sqlalchemy import select

from app.bottec_bot.db.repo import get_session
from app.bottec_bot.db.models import TelegramResource, User
from app.bottec_bot.logging.setup import loggers
from app.bottec_bot.logging.decorators import catch_exception

logger = loggers['bot']


@catch_exception(logger, 'Error in get_or_create_user')
async def get_or_create_user(tg_user: TelegramUser) -> User:
    async with get_session() as session:
        user = await session.get(User, tg_user.id)
        if user is None:
            user = User(
                id=tg_user.id,
                username=tg_user.username,
            )
            session.add(user)
            logger.info(f'New user created: id={tg_user.id}, username={tg_user.username}')
        else:
            logger.debug(f'Existing user loaded: id={tg_user.id}')
        return user


@catch_exception(logger, 'Error while fetching Telegram resources')
async def get_required_resources() -> list[TelegramResource]:
    async with get_session() as session:
        stmt = select(TelegramResource)
        result = await session.execute(stmt)
        resources = result.scalars().all()
        logger.debug(f'{len(resources)} Telegram resources fetched')
        return resources
