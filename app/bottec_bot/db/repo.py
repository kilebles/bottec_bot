from contextlib import asynccontextmanager

from app.bottec_bot.db.session import AsyncSessionLocal
from app.bottec_bot.logging.setup import loggers

logger = loggers['bot']


@asynccontextmanager
async def get_session():
    session = AsyncSessionLocal()
    try:
        logger.debug('New DB session started')
        yield session
        await session.commit()
        logger.debug('DB session committed')
    except Exception as e:
        await session.rollback()
        logger.exception(f'DB session rolled back due to: {e}')
        raise
    finally:
        await session.close()
        logger.debug('DB session closed')