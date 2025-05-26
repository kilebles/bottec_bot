from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from app.bottec_bot.services.catalog import (
    get_all_categories,
    get_subcategories_by_category,
)
from app.bottec_bot.UI.keyboards import (
    category_keyboard_paginated,
    subcategory_keyboard_paginated,
)

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



