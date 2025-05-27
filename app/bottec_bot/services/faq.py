from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.bottec_bot.db.models import FAQ


async def get_faq_by_key(session: AsyncSession, key: str) -> FAQ | None:
    result = await session.execute(select(FAQ).where(FAQ.key == key))
    return result.scalar_one_or_none()


async def get_all_faqs(session: AsyncSession) -> list[FAQ]:
    result = await session.execute(select(FAQ))
    return result.scalars().all()