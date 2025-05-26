from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

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
from app.bottec_bot.utils.safe import safe_edit_or_resend

router = Router()


@router.callback_query(F.data == 'open_catalog')
async def show_categories(callback: CallbackQuery):
    categories = await get_all_categories()
    await callback.message.edit_text(
        'Выберите категорию:',
        reply_markup=category_keyboard_paginated(categories, page=1)
    )


@router.callback_query(F.data.startswith('cat_page_'))
async def show_categories_page(callback: CallbackQuery):
    page = int(callback.data.split('_')[-1])
    categories = await get_all_categories()
    await callback.message.edit_reply_markup(
        reply_markup=category_keyboard_paginated(categories, page=page)
    )


@router.callback_query(lambda c: c.data.startswith('cat_') and not c.data.startswith('cat_page_'))
async def show_subcategories(callback: CallbackQuery):
    cat_id = int(callback.data.split('_')[1])
    subcats = await get_subcategories_by_category(cat_id)
    try:
        await callback.message.edit_text(
            'Выберите подкатегорию:',
            reply_markup=subcategory_keyboard_paginated(subcats, category_id=cat_id, page=1)
        )
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e):
            raise


@router.callback_query(F.data.startswith('sub_'))
async def show_products_from_subcategory(callback: CallbackQuery):
    '''
    Отображение товаров в подкатегории
    '''
    subcat_id = int(callback.data.split('_')[1])
    products = await get_products_by_subcategory(subcat_id)

    if not products:
        await callback.answer('В этой подкатегории пока нет товаров', show_alert=True)
        return

    await callback.message.delete()

    await callback.message.answer(
        'Выберите товар:',
        reply_markup=product_keyboard_paginated(
            products,
            subcategory_id=subcat_id,
            page=1
        )
    )
    

@router.callback_query(F.data.startswith('product_'))
async def show_product_detail(callback: CallbackQuery):
    product_id = int(callback.data.split('_')[1])
    product = await get_product_by_id(product_id)

    if not product:
        await callback.answer('Товар не найден', show_alert=True)
        return

    text = (
        f'<b>{product.title}</b>\n\n'
        f'{product.description or "Без описания"}\n\n'
        f'<b>Цена:</b> {product.price}₽'
    )

    await callback.message.answer_photo(
        photo=product.photo_url,
        caption=text,
        parse_mode='HTML',
        reply_markup=product_detail_keyboard(
            subcategory_id=product.subcategory_id,
            product_id=product.id
        )
    )