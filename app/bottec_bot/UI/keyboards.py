from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bottec_bot.data.faq_data import faq_dict



def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🛍 Каталог', callback_data='open_catalog')],
        [InlineKeyboardButton(text='🧺 Корзина', callback_data='open_cart')],
        [InlineKeyboardButton(text='❓ FAQ', callback_data='faq_main')]
    ])
    
    
def faq_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text=faq_dict[key]['title'], callback_data=f'faq_{key}')]
        for key in faq_dict
    ]
    keyboard.append([InlineKeyboardButton(text='🏠 Главное меню', callback_data='main_menu')])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def back_to_main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='🏠 Главное меню', callback_data='main_menu')]
        ]
    )