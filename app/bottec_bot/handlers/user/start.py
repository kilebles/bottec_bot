from aiogram import Bot, Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from app.bottec_bot.services.start import get_or_create_user, get_required_resources
from app.bottec_bot.UI.keyboards import main_menu_keyboard
from app.bottec_bot.logging.setup import loggers

logger = loggers['bot']

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    from_user = message.from_user
    user_id = from_user.id

    await get_or_create_user(from_user)
    logger.info(f'User started bot: id={user_id}, username={from_user.username}')

    resources = await get_required_resources()
    logger.debug(f'{len(resources)} subscription resources loaded for user {user_id}')

    if not resources:
        await message.answer('⚠️ Нет ресурсов для подписки.')
        logger.warning(f'No subscription resources available for user {user_id}')
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
    resources = await get_required_resources()
    logger.debug(f'Checking subscription for user {user_id}, {len(resources)} resources')

    for res in resources:
        try:
            member = await bot.get_chat_member(res.tg_id, user_id)
            if member.status in ('left', 'kicked'):
                raise ValueError()
        except Exception:
            logger.info(f'User {user_id} is not subscribed to {res.name} ({res.tg_id})')
            await callback.answer('❌ Подпишитесь на все сообщества.', show_alert=True)
            return

    logger.info(f'User {user_id} passed subscription check')
    await callback.message.edit_text(
        '🏠 Главное меню',
        reply_markup=main_menu_keyboard(),
        parse_mode='HTML'
    )


@router.callback_query(F.data == 'main_menu')
async def show_main_menu(callback: CallbackQuery):
    user_id = callback.from_user.id
    logger.debug(f'User {user_id} opened main menu')

    await callback.message.delete()
    await callback.message.answer(
        '🏠 Главное меню:',
        reply_markup=main_menu_keyboard()
    )
