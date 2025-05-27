from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bottec_bot.UI.keyboards import main_menu_keyboard
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
            select(CartItem)
            .where(CartItem.user_id == user_id)
            .options(joinedload(CartItem.product))
        )
        return result.scalars().all()



async def remove_from_cart(cart_item_id: int):
    async with get_session() as session:
        await session.execute(
            delete(CartItem).where(CartItem.id == cart_item_id)
        )


async def render_cart(callback: CallbackQuery, page: int = 1):
    tg_id = callback.from_user.id
    cart_items = await get_cart_items(tg_id)

    if not cart_items:
        await callback.message.edit_text('🧺 Ваша корзина пуста', reply_markup=main_menu_keyboard())
        return

    PAGE_SIZE = 3
    total_pages = (len(cart_items) + PAGE_SIZE - 1) // PAGE_SIZE
    start = (page - 1) * PAGE_SIZE
    end = start + PAGE_SIZE
    current_items = cart_items[start:end]

    text_lines = ['🧾 <b>Содержимое корзины:</b>\n']
    for item in current_items:
        text_lines.append(
            f'• <b>{item.product.title}</b> — {item.quantity} шт. — {item.product.price * item.quantity:.2f}₽\n\n'
        )
    total = sum(item.product.price * item.quantity for item in cart_items)
    text_lines.append(f'\n<b>К оплате:</b> {total:.2f}₽')

    keyboard = []
    for item in current_items:
        keyboard.append([
            InlineKeyboardButton(
                text=f'❌ Удалить «{item.product.title[:20]}»',
                callback_data=f'remove_cart_item_{item.id}'
            )
        ])

    nav_buttons = []
    if page > 1:
        nav_buttons.append(InlineKeyboardButton(text='◀ Назад', callback_data=f'open_cart_{page - 1}'))
    if page < total_pages:
        nav_buttons.append(InlineKeyboardButton(text='Вперёд ▶', callback_data=f'open_cart_{page + 1}'))
    if nav_buttons:
        keyboard.append(nav_buttons)

    keyboard.append([InlineKeyboardButton(text='🏠 Главное меню', callback_data='main_menu')])

    await callback.message.edit_text(
        '\n'.join(text_lines),
        parse_mode='HTML',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
    )