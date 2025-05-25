from aiogram import Bot
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from app.bottec_bot.config import config
from app.bottec_bot.UI.keyboards import main_menu_keyboard

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🔁 Проверить подписку', callback_data='check_subscription')]
    ])
    text = (
        'Привет! Чтобы продолжить, подпишитесь на:\n'
        f'📢 [канал]({config.CHANNEL_LINK})\n'
        f'💬 [группу]({config.GROUP_LINK})'
    )
    await message.answer(text, reply_markup=kb, parse_mode='Markdown')


@router.callback_query(F.data == 'check_subscription')
async def check_subscription(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    for chat_id in [config.CHANNEL_ID, config.GROUP_ID]:  # TODO: Проверять через админку
        member = await bot.get_chat_member(chat_id, user_id)
        if member.status in ('left', 'kicked'):
            await callback.answer('❌ Подпишитесь на оба сообщества.', show_alert=True)
            return
    await callback.message.edit_text(  # type: ignore
        '🏠 Главное меню',
        reply_markup=main_menu_keyboard(),
        parse_mode='HTML'
    )


@router.callback_query(F.data == 'main_menu')
async def show_main_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        '🏠 Главное меню',
        reply_markup=main_menu_keyboard()
    )