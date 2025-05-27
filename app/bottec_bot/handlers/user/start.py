from aiogram import Bot
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from bottec_bot.db.repo import get_session
from bottec_bot.services.start import get_or_create_user, get_required_resources
from app.bottec_bot.UI.keyboards import main_menu_keyboard

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    from_user = message.from_user

    async with get_session() as session:
        await get_or_create_user(session, from_user)
        resources = await get_required_resources(session)

    if not resources:
        await message.answer('⚠️ Нет ресурсов для подписки.')
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🔁 Проверить подписку', callback_data='check_subscription')]
    ])

    text_lines = ['Привет! Чтобы продолжить, подпишитесь на:']
    for res in resources:
        text_lines.append(f'🔗 [{res.name}]({res.link})')

    await message.answer('\n'.join(text_lines), reply_markup=kb, parse_mode='Markdown')


@router.callback_query(F.data == 'check_subscription')
async def check_subscription(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id

    async with get_session() as session:
        resources = await get_required_resources(session)

    for res in resources:
        try:
            member = await bot.get_chat_member(res.tg_id, user_id)
            if member.status in ('left', 'kicked'):
                raise ValueError()
        except Exception:
            await callback.answer('❌ Подпишитесь на все сообщества.', show_alert=True)
            return

    await callback.message.edit_text(
        '🏠 Главное меню',
        reply_markup=main_menu_keyboard(),
        parse_mode='HTML'
    )


@router.callback_query(F.data == 'main_menu')
async def show_main_menu(callback: CallbackQuery):
    '''
    delete так как edit_text не работает + 
    поднимает чатбота в списке чатов  наверх 
    '''
    await callback.message.delete()
    await callback.message.answer(
        '🏠 Главное меню:',
        reply_markup=main_menu_keyboard()
    )