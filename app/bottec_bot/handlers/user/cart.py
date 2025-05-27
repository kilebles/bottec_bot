from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from app.bottec_bot.utils.payment import create_yoomoney_payment
from app.bottec_bot.states import CartStates, OrderStates
from app.bottec_bot.UI.keyboards import main_menu_keyboard, back_to_main_keyboard, order_payment_keyboard
from app.bottec_bot.services.cart import add_to_cart, get_cart_items, remove_from_cart, render_cart
from app.bottec_bot.logging.setup import loggers

logger = loggers['bot']

router = Router()


@router.callback_query(F.data.startswith('add_to_cart_'))
async def ask_quantity(callback: CallbackQuery, state: FSMContext):
    product_id = int(callback.data.split('_')[-1])
    await state.update_data(product_id=product_id)
    await state.set_state(CartStates.waiting_for_quantity)
    logger.debug(f'User {callback.from_user.id} selected product_id={product_id} to add to cart')
    await callback.message.answer('Введите количество товара:', reply_markup=back_to_main_keyboard())


@router.message(F.text.isdigit(), CartStates.waiting_for_quantity)
async def save_to_cart(message: Message, state: FSMContext):
    data = await state.get_data()
    product_id = data['product_id']
    quantity = int(message.text)
    tg_id = message.from_user.id

    await add_to_cart(tg_id, product_id, quantity)
    logger.info(f'User {tg_id} added product_id={product_id} quantity={quantity} to cart')

    await state.clear()
    await message.answer('🧺 Товар добавлен в корзину', reply_markup=main_menu_keyboard())


@router.callback_query(F.data.startswith('open_cart'))
async def show_cart(callback: CallbackQuery):
    page = 1
    if '_' in callback.data:
        try:
            page = int(callback.data.split('_')[-1])
        except ValueError:
            logger.warning(f'Invalid cart page value: {callback.data}')
            pass

    logger.debug(f'User {callback.from_user.id} opened cart page {page}')
    await render_cart(callback, page)


@router.callback_query(F.data.startswith('remove_cart_item_'))
async def handle_remove_item(callback: CallbackQuery):
    try:
        item_id = int(callback.data.split('_')[-1])
        await remove_from_cart(item_id)
        logger.info(f'User {callback.from_user.id} removed cart_item_id={item_id}')
        await callback.answer('❌ Товар удалён')
        await render_cart(callback, page=1)
    except Exception as e:
        logger.exception(f'Error removing cart item: {e}')
        await callback.answer('Ошибка при удалении', show_alert=True)


@router.callback_query(F.data == 'start_order')
async def ask_address(callback: CallbackQuery, state: FSMContext):
    await state.set_state(OrderStates.waiting_for_address)
    logger.debug(f'User {callback.from_user.id} started order process')
    await callback.message.edit_text('📍 Пожалуйста, введите адрес доставки:')


@router.message(OrderStates.waiting_for_address)
async def receive_address(message: Message, state: FSMContext):
    address = message.text
    tg_id = message.from_user.id

    logger.debug(f'User {tg_id} entered address: {address}')
    await state.clear()

    cart_items = await get_cart_items(tg_id)
    total = sum(item.product.price * item.quantity for item in cart_items)

    try:
        payment = await create_yoomoney_payment(
            value=f'{total:.2f}',
            description='Оплата заказа',
            tg_id=tg_id
        )
        url = payment['confirmation']['confirmation_url']
        logger.info(f'Payment created for user {tg_id}, amount={total:.2f}')
    except Exception as e:
        logger.exception(f'Payment creation failed for user {tg_id}: {e}')
        await message.answer('Произошла ошибка при создании платежа. Попробуйте позже.')
        return

    await message.answer(
        f'📦 Ваш заказ оформлен!\n\n🚚 Адрес доставки: <b>{address}</b>\n💰 К оплате: <b>{total:.2f}₽</b>',
        reply_markup=order_payment_keyboard(url),
        parse_mode='HTML'
    )
