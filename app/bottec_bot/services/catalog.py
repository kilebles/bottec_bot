from sqlalchemy import select

from app.bottec_bot.db.models import Category, Subcategory
from app.bottec_bot.db.repo import get_session


async def get_all_categories():
    async with get_session() as session:
        result = await session.execute(select(Category))
        return result.scalars().all()


async def get_subcategories_by_category(category_id: int):
    async with get_session() as session:
        result = await session.execute(
            select(Subcategory).where(Subcategory.category_id == category_id)
        )
        return result.scalars().all()
