from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineQuery, InlineQueryResultArticle, InputTextMessageContent

from app.bottec_bot.UI.keyboards import back_to_main_keyboard, faq_keyboard_paginated
from app.bottec_bot.services.faq import get_faq_by_key, get_all_faqs

router = Router()


@router.callback_query(F.data == 'faq_main')
async def show_faq_menu(callback: CallbackQuery):
    faqs = await get_all_faqs()
    await callback.message.edit_text('Выберите вопрос:', reply_markup=faq_keyboard_paginated(faqs, page=1))


@router.callback_query(lambda c: c.data.startswith('faq_') and not c.data.startswith('faq_page_'))
async def show_faq_answer(callback: CallbackQuery):
    key = callback.data.removeprefix('faq_')
    faq = await get_faq_by_key(key)
    
    if not faq:
        await callback.answer('Вопрос не найден.', show_alert=True)
        return
    await callback.message.edit_text(
        text=faq.text,
        reply_markup=back_to_main_keyboard()
    )


@router.callback_query(F.data.startswith('faq_page_'))
async def handle_faq_page(callback: CallbackQuery):
    page = int(callback.data.split('_')[-1])
    faqs = await get_all_faqs()
    await callback.message.edit_reply_markup(reply_markup=faq_keyboard_paginated(faqs, page))


@router.inline_query()
async def handle_inline_faq(query: InlineQuery):
    query_text = query.query.strip().lower()
    faqs = await get_all_faqs()

    results = []
    for faq in faqs:
        if query_text in faq.title.lower() or query_text == '':
            results.append(
                InlineQueryResultArticle(
                    id=faq.key,
                    title=faq.title,
                    description=faq.text[:50] + '...',
                    input_message_content=InputTextMessageContent(
                        message_text=faq.text
                    )
                )
            )
    await query.answer(results, cache_time=1)
