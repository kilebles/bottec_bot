from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineQuery, InlineQueryResultArticle, InputTextMessageContent

from app.bottec_bot.UI.keyboards import back_to_main_keyboard, faq_keyboard_paginated
from app.bottec_bot.data.faq_data import faq_dict  # TODO: Сейчас хардкод из data, потом поменять на БД

router = Router()


@router.callback_query(F.data == 'faq_main')
async def show_faq_menu(callback: CallbackQuery):
    await callback.message.edit_text('Выберите вопрос:', reply_markup=faq_keyboard_paginated(page=1))


@router.callback_query(lambda c: c.data.startswith('faq_') and not c.data.startswith('faq_page_'))
async def show_faq_answer(callback: CallbackQuery):
    key = callback.data.removeprefix('faq_')
    answer = faq_dict.get(key)
    if not answer:
        await callback.answer('Вопрос не найден.', show_alert=True)
        return
    await callback.message.edit_text(
        text=answer['text'],
        reply_markup=back_to_main_keyboard()
    )


@router.callback_query(F.data.startswith('faq_page_'))
async def handle_faq_page(callback: CallbackQuery):
    page = int(callback.data.split('_')[-1])
    await callback.message.edit_reply_markup(reply_markup=faq_keyboard_paginated(page))
    
    
@router.inline_query()
async def handle_inline_faq(query: InlineQuery):
    '''
    Автодополнение для inline-запросов из строки ввода (@botname вопрос).
    Возвращает список по частичному совпадению.
    '''
    query_text = query.query.strip().lower()
    results = []

    for key, item in faq_dict.items():
        title = item['title']
        if query_text in title.lower() or query_text == '':
            results.append(
                InlineQueryResultArticle(
                    id=key,
                    title=title,
                    description=item['text'][:50] + '...',
                    input_message_content=InputTextMessageContent(
                        message_text=item['text']
                    )
                )
            )
    await query.answer(results, cache_time=1)