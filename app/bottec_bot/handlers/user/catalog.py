from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from app.bottec_bot.services.catalog import (
    get_all_categories,
    get_product_by_id,
    get_products_by_subcategory,
    get_subcategories_by_category,
)
from app.bottec_bot.UI.keyboards import (
    category_keyboard_paginated,
    product_detail_keyboard,
    product_keyboard_paginated,
    subcategory_keyboard_paginated,
)

from app.bottec_bot.states import CartStates
from app.bottec_bot.logging.setup import loggers

logger = loggers['bot']

router = Router()


@router.callback_query(F.data == 'open_catalog')
async def show_categories(callback: CallbackQuery):
    categories = await get_all_categories()
    logger.debug(f'User {callback.from_user.id} opened catalog root ({len(categories)} categories found)')
    await callback.message.edit_text(
        'Выберите категорию:',
        reply_markup=category_keyboard_paginated(categories, page=1)
    )


@router.callback_query(F.data.startswith('cat_page_'))
async def show_categories_page(callback: CallbackQuery):
    page = int(callback.data.split('_')[-1])
    categories = await get_all_categories()
    logger.debug(f'User {callback.from_user.id} paged to category page {page}')
    await callback.message.edit_reply_markup(
        reply_markup=category_keyboard_paginated(categories, page=page)
    )


@router.callback_query(lambda c: c.data.startswith('cat_') and not c.data.startswith('cat_page_'))
async def show_subcategories(callback: CallbackQuery):
    cat_id = int(callback.data.split('_')[1])
    subcats = await get_subcategories_by_category(cat_id)
    logger.debug(f'User {callback.from_user.id} opened category {cat_id} ({len(subcats)} subcategories)')

    try:
        await callback.message.edit_text(
            'Выберите подкатегорию:',
            reply_markup=subcategory_keyboard_paginated(subcats, category_id=cat_id, page=1)
        )
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e):
            logger.exception(f'TelegramBadRequest while editing message for category {cat_id}: {e}')
            raise
        else:
            logger.warning(f'Message not modified for category {cat_id}')


@router.callback_query(F.data.startswith('sub_'))
async def show_products_from_subcategory(callback: CallbackQuery):
    subcat_id = int(callback.data.split('_')[1])
    products = await get_products_by_subcategory(subcat_id)
    logger.debug(f'User {callback.from_user.id} opened subcategory {subcat_id} ({len(products)} products)')

    if not products:
        await callback.answer('В этой подкатегории пока нет товаров', show_alert=True)
        logger.info(f'User {callback.from_user.id} opened empty subcategory {subcat_id}')
        return

    await callback.message.delete()
    await callback.message.answer(
        'Выберите товар:',
        reply_markup=product_keyboard_paginated(products, subcategory_id=subcat_id, page=1)
    )


@router.callback_query(F.data.startswith('product_'))
async def show_product_detail(callback: CallbackQuery):
    product_id = int(callback.data.split('_')[1])
    product = await get_product_by_id(product_id)

    if not product:
        await callback.answer('Товар не найден', show_alert=True)
        logger.warning(f'Product not found: product_id={product_id}')
        return

    logger.debug(f'User {callback.from_user.id} viewed product {product_id}')

    text = (
        f'<b>{product.title}</b>\n\n'
        f'<blockquote expandable>{product.description or "Без описания"}</blockquote>\n\n'
        f'<b>Цена:</b> {product.price}₽'
    )

    await callback.message.delete()
    await callback.message.answer_photo(
        photo=product.photo_url,
        caption=text,
        parse_mode='HTML',
        reply_markup=product_detail_keyboard(
            subcategory_id=product.subcategory_id,
            product_id=product.id
        )
    )


@router.callback_query(F.data.startswith('add_to_cart_'))
async def ask_quantity(callback: CallbackQuery, state: FSMContext):
    product_id = int(callback.data.split('_')[-1])
    await state.update_data(product_id=product_id)
    await state.set_state(CartStates.waiting_for_quantity)

    logger.debug(f'User {callback.from_user.id} selected product {product_id} for quantity input')

    await callback.message.delete()
    await callback.message.answer('Введите количество товара:')
