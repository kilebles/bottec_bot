from sqlalchemy import select

from app.bottec_bot.db.models import FAQ
from app.bottec_bot.db.repo import get_session


async def get_faq_by_key(key: str) -> FAQ | None:
    async with get_session() as session:
        result = await session.execute(select(FAQ).where(FAQ.key == key))
        return result.scalar_one_or_none()


async def get_all_faqs() -> list[FAQ]:
    async with get_session() as session:
        result = await session.execute(select(FAQ))
        return result.scalars().all()