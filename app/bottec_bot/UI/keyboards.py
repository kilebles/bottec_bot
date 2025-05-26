from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from math import ceil
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bottec_bot.data.faq_data import faq_dict


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🛍 Каталог', callback_data='open_catalog')],
        [InlineKeyboardButton(text='🧺 Корзина', callback_data='open_cart')],
        [InlineKeyboardButton(text='❓ FAQ', callback_data='faq_main')]
    ])
    

def back_to_main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='🏠 Главное меню', callback_data='main_menu')]
        ]
    )


def paginate_keyboard(
    items: list,
    page: int,
    page_size: int,
    item_callback_prefix: str,
    item_text_getter=lambda x: str(x),
    item_id_getter=lambda x: str(x),
    back_callback: str | None = None,
    back_text: str = '🏠 Главное меню',
    page_callback_prefix: str | None = None
) -> InlineKeyboardMarkup:
    total_pages = ceil(len(items) / page_size)
    start = (page - 1) * page_size
    end = start + page_size
    page_items = items[start:end]

    keyboard = [
        [
            InlineKeyboardButton(
                text=item_text_getter(item),
                callback_data=f'{item_callback_prefix}_{item_id_getter(item)}'
            )
        ]
        for item in page_items
    ]

    nav_buttons = []
    if page > 1:
        nav_buttons.append(
            InlineKeyboardButton(
                text='◀ Назад',
                callback_data=f'{page_callback_prefix}_{page - 1}' if page_callback_prefix else f'{item_callback_prefix}_page_{page - 1}'
            )
        )
    if page < total_pages:
        nav_buttons.append(
            InlineKeyboardButton(
                text='Вперёд ▶',
                callback_data=f'{page_callback_prefix}_{page + 1}' if page_callback_prefix else f'{item_callback_prefix}_page_{page + 1}'
            )
        )
    if nav_buttons:
        keyboard.append(nav_buttons)

    if back_callback:
        keyboard.append(
            [InlineKeyboardButton(text=back_text, callback_data=back_callback)]
        )
    print(f'page={page}, total_pages={total_pages}, items={len(items)}')
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
    

def category_keyboard_paginated(categories: list, page: int = 1):
    return paginate_keyboard(
        items=categories,
        page=page,
        page_size=5,
        item_callback_prefix='cat',
        item_text_getter=lambda c: c.name,
        item_id_getter=lambda c: c.id,
        back_callback='main_menu',
        page_callback_prefix='cat_page'
    )


def subcategory_keyboard_paginated(subcategories: list, category_id: int, page: int = 1):
    return paginate_keyboard(
        items=subcategories,
        page=page,
        page_size=5,
        item_callback_prefix='sub',
        item_text_getter=lambda s: s.name,
        item_id_getter=lambda s: s.id,
        back_callback=f'cat_{category_id}',
        page_callback_prefix=f'sub_page_{category_id}'
    )


def faq_keyboard_paginated(page: int = 1):
    items = list(faq_dict.items())

    return paginate_keyboard(
        items=items,
        page=page,
        page_size=5,
        item_callback_prefix='faq',
        item_text_getter=lambda item: item[1]['title'],
        item_id_getter=lambda item: item[0],
        back_callback='main_menu',
        page_callback_prefix='faq_page'
    )


