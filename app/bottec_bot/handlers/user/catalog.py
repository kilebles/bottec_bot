from aiogram import Router, F
from aiogram.types import CallbackQuery

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


@router.callback_query(F.data.startswith('cat_'))
async def show_subcategories(callback: CallbackQuery):
    cat_id = int(callback.data.split('_')[1])
    subcats = await get_subcategories_by_category(cat_id)
    await callback.message.edit_text(
        'Выберите подкатегорию:',
        reply_markup=subcategory_keyboard_paginated(subcats, category_id=cat_id, page=1)
    )
