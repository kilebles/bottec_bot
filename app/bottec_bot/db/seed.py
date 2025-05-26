import asyncio

from app.bottec_bot.db.models import Category, Subcategory
from app.bottec_bot.db.session import AsyncSessionLocal


# TODO: Эту логику перенести в админку, seed.py - убрать
async def seed_categories():
    async with AsyncSessionLocal() as session:
        categories = [
            Category(name='Ноутбуки'),
            Category(name='Смартфоны'),
            Category(name='Аксессуары'),
            Category(name='Планшеты'),
            Category(name='Умные часы'),
            Category(name='Наушники'),
            Category(name='Мониторы'),
            Category(name='Клавиатуры'),
            Category(name='Мыши'),
            Category(name='Сетевое оборудование'),
        ]

        session.add_all(categories)
        await session.flush()

        subcategories = []
        for category in categories:
            subcategories.append(Subcategory(name=f'{category.name} — Бюджетные', category_id=category.id))
            subcategories.append(Subcategory(name=f'{category.name} — Премиум', category_id=category.id))

        session.add_all(subcategories)
        await session.commit()


if __name__ == '__main__':
    asyncio.run(seed_categories())
