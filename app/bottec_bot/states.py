from aiogram.fsm.state import StatesGroup, State


class CartStates(StatesGroup):
    waiting_for_quantity = State()
    

class OrderStates(StatesGroup):
    waiting_for_address = State()