from sqlalchemy import select, delete

from app.bottec_bot.db.models import CartItem
from app.bottec_bot.db.repo import get_session


async def add_to_cart(user_id: int, product_id: int, quantity: int):
    async with get_session() as session:
        result = await session.execute(
            select(CartItem).where(
                CartItem.user_id == user_id,
                CartItem.product_id == product_id
            )
        )
        item = result.scalar_one_or_none()
        if item:
            item.quantity += quantity
        else:
            item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
            session.add(item)


async def get_cart_items(user_id: int):
    async with get_session() as session:
        result = await session.execute(
            select(CartItem).where(CartItem.user_id == user_id)
        )
        return result.scalars().all()


async def remove_from_cart(cart_item_id: int):
    async with get_session() as session:
        await session.execute(
            delete(CartItem).where(CartItem.id == cart_item_id)
        )
