from sqlalchemy import select

from app.bottec_bot.db.models import Category, Product, Subcategory
from app.bottec_bot.db.repo import get_session
from app.bottec_bot.logging.setup import loggers
from app.bottec_bot.logging.decorators import catch_exception

logger = loggers['bot']


@catch_exception(logger, 'Error while fetching all categories')
async def get_all_categories():
    async with get_session() as session:
        result = await session.execute(select(Category))
        categories = result.scalars().all()
        logger.debug(f'{len(categories)} categories fetched')
        return categories


@catch_exception(logger, 'Error while fetching subcategories by category_id')
async def get_subcategories_by_category(category_id: int):
    async with get_session() as session:
        result = await session.execute(
            select(Subcategory).where(Subcategory.category_id == category_id)
        )
        subcategories = result.scalars().all()
        logger.debug(f'{len(subcategories)} subcategories fetched for category_id={category_id}')
        return subcategories


@catch_exception(logger, 'Error while fetching products by subcategory_id')
async def get_products_by_subcategory(subcategory_id: int):
    async with get_session() as session:
        result = await session.execute(
            select(Product).where(Product.subcategory_id == subcategory_id)
        )
        products = result.scalars().all()
        logger.debug(f'{len(products)} products fetched for subcategory_id={subcategory_id}')
        return products


@catch_exception(logger, 'Error while fetching product by id')
async def get_product_by_id(product_id: int) -> Product | None:
    async with get_session() as session:
        result = await session.execute(
            select(Product).where(Product.id == product_id)
        )
        product = result.scalar_one_or_none()
        if product:
            logger.debug(f'Product fetched: id={product_id}, title="{product.title}"')
        else:
            logger.debug(f'No product found with id={product_id}')
        return product
