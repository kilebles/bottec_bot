from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from app.bottec_bot.states import CartStates
from app.bottec_bot.UI.keyboards import main_menu_keyboard, back_to_main_keyboard
from app.bottec_bot.services.cart import add_to_cart, get_cart_items, remove_from_cart

router = Router()


@router.callback_query(F.data.startswith('add_to_cart_'))
async def ask_quantity(callback: CallbackQuery, state: FSMContext):
    product_id = int(callback.data.split('_')[-1])
    await state.update_data(product_id=product_id)
    await state.set_state(CartStates.waiting_for_quantity)
    await callback.message.answer('Введите количество товара:', reply_markup=back_to_main_keyboard())


@router.message(F.text.isdigit(), CartStates.waiting_for_quantity)
async def save_to_cart(message: Message, state: FSMContext):
    data = await state.get_data()
    product_id = data['product_id']
    quantity = int(message.text)
    tg_id = message.from_user.id

    await add_to_cart(tg_id, product_id, quantity)

    await state.clear()
    await message.answer('🧺 Товар добавлен в корзину', reply_markup=main_menu_keyboard())


@router.callback_query(F.data == 'open_cart')
async def show_cart(callback: CallbackQuery):
    tg_id = callback.from_user.id
    cart_items = await get_cart_items(tg_id)

    if not cart_items:
        await callback.message.answer('🧺 Ваша корзина пуста', reply_markup=main_menu_keyboard())
        return

    text_lines = ['🧾 <b>Содержимое корзины:</b>\n']
    for item in cart_items:
        text_lines.append(f'• <b>{item.product.title}</b> — {item.quantity} шт. — {item.product.price * item.quantity}₽\n'
                          f'/remove_{item.id}')
    total = sum(item.product.price * item.quantity for item in cart_items)
    text_lines.append(f'\n<b>Итого:</b> {total}₽')

    await callback.message.answer('\n'.join(text_lines), reply_markup=main_menu_keyboard())


@router.message(F.text.startswith('/remove_'))
async def remove_item(message: Message):
    try:
        item_id = int(message.text.split('_')[-1])
        await remove_from_cart(item_id)
        await message.answer('❌ Товар удалён из корзины')
    except ValueError:
        await message.answer('Некорректный ID товара')
