from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from app.bottec_bot.UI.keyboards import main_menu_keyboard
from app.bottec_bot.db.models import CartItem
from app.bottec_bot.db.repo import get_session
from app.bottec_bot.logging.setup import loggers
from app.bottec_bot.logging.decorators import catch_exception

logger = loggers['bot']


@catch_exception(logger, 'Error while adding item to cart')
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
            logger.info(f'Cart item updated: user_id={user_id}, product_id={product_id}, quantity+={quantity}')
        else:
            item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
            session.add(item)
            logger.info(f'Cart item created: user_id={user_id}, product_id={product_id}, quantity={quantity}')


@catch_exception(logger, 'Error while retrieving cart items')
async def get_cart_items(user_id: int):
    async with get_session() as session:
        result = await session.execute(
            select(CartItem)
            .where(CartItem.user_id == user_id)
            .options(joinedload(CartItem.product))
        )
        items = result.scalars().all()
        logger.debug(f'{len(items)} items retrieved from cart for user_id={user_id}')
        return items


@catch_exception(logger, 'Error while removing item from cart')
async def remove_from_cart(cart_item_id: int):
    async with get_session() as session:
        await session.execute(
            delete(CartItem).where(CartItem.id == cart_item_id)
        )
        logger.info(f'Cart item removed: cart_item_id={cart_item_id}')


@catch_exception(logger, 'Error while rendering cart')
async def render_cart(callback: CallbackQuery, page: int = 1):
    tg_id = callback.from_user.id
    cart_items = await get_cart_items(tg_id)

    if not cart_items:
        logger.debug(f'User {tg_id} opened empty cart')
        await callback.message.edit_text('🧺 Ваша корзина пуста', reply_markup=main_menu_keyboard())
        return

    PAGE_SIZE = 3
    total_pages = (len(cart_items) + PAGE_SIZE - 1) // PAGE_SIZE
    start = (page - 1) * PAGE_SIZE
    end = start + PAGE_SIZE
    current_items = cart_items[start:end]

    logger.debug(
        f'Rendering cart for user_id={tg_id}, page={page}/{total_pages}, items_on_page={len(current_items)}'
    )

    text_lines = ['🧾 <b>Ваша корзина:</b>\n']
    for item in current_items:
        text_lines.append(
            f'<blockquote>🗑 {item.product.title}</blockquote>  {item.quantity} шт. 💵 {item.product.price * item.quantity:.2f}₽\n'
        )
    total = sum(item.product.price * item.quantity for item in cart_items)
    text_lines.append(f'\n<b>К оплате:</b> {total:.2f}₽')

    keyboard = []
    for item in current_items:
        keyboard.append([InlineKeyboardButton(
            text=f'❌ Удалить “{item.product.title[:20]}”',
            callback_data=f'remove_cart_item_{item.id}'
        )])

    nav_buttons = []
    if page > 1:
        nav_buttons.append(InlineKeyboardButton(text='◀ Назад', callback_data=f'open_cart_{page - 1}'))
    if page < total_pages:
        nav_buttons.append(InlineKeyboardButton(text='Вперед ▶', callback_data=f'open_cart_{page + 1}'))
    if nav_buttons:
        keyboard.append(nav_buttons)

    keyboard.append([
        InlineKeyboardButton(text='🚚 Заказать', callback_data='start_order')
    ])
    keyboard.append([
        InlineKeyboardButton(text='🏠 Главное меню', callback_data='main_menu')
    ])

    await callback.message.edit_text(
        '\n'.join(text_lines),
        parse_mode='HTML',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
    )
