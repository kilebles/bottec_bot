from sqlalchemy import select

from app.bottec_bot.db.models import FAQ
from app.bottec_bot.db.repo import get_session
from app.bottec_bot.logging.setup import loggers
from app.bottec_bot.logging.decorators import catch_exception

logger = loggers['bot']


@catch_exception(logger, 'Error while fetching FAQ by key')
async def get_faq_by_key(key: str) -> FAQ | None:
    async with get_session() as session:
        result = await session.execute(select(FAQ).where(FAQ.key == key))
        faq = result.scalar_one_or_none()
        if faq:
            logger.debug(f'FAQ found for key="{key}"')
        else:
            logger.debug(f'No FAQ found for key="{key}"')
        return faq


@catch_exception(logger, 'Error while fetching all FAQs')
async def get_all_faqs() -> list[FAQ]:
    async with get_session() as session:
        result = await session.execute(select(FAQ))
        faqs = result.scalars().all()
        logger.debug(f'{len(faqs)} FAQ entries fetched')
        return faqs
