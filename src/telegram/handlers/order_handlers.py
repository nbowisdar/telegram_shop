from setup import order_router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command, Text
from aiogram import F
from src.telegram.buttons import user_main_btn, build_goods_with_price_inl, categories_inl
import decimal
from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from src.telegram.handlers.user_handlers import user_router
from src.telegram.buttons import user_main_btn

"""
class OrderModel(NamedTuple):
    time_created: datetime
    ordered_goods: GoodsModel
    amount: int
    user: UserModel
    with_discount: bool
    note: str | None = None
"""


class GoodsState(StatesGroup):
    ordered_goods = State()
    amount = State()
    user = State()
    with_discount = State()
    note = State()
    block_input = State()


@user_router.message(GoodsState.block_input)
async def new_order(message: Message):
    await message.delete()


@order_router.message(F.text == "🛒 Обрати товар")
async def new_order(message: Message, state: FSMContext):
    await state.set_state(GoodsState.block_input)
    await message.answer('Генерація нового замовлення 👇', reply_markup=ReplyKeyboardRemove())
    await message.answer("Оберіть категорію", reply_markup=categories_inl())


@user_router.callback_query(Text(startswith="order_drop"))
async def anon(callback: CallbackQuery, state: FSMContext):
    _, action = callback.data.split("|")
    await state.clear()
    await callback.message.delete()
    if action == "cancel":
        await callback.message.answer("❌ Скасовано ❌", reply_markup=user_main_btn)
        return
    await new_order(callback.message, state)


@user_router.callback_query(Text(startswith="new_order_cat"))
async def anon(callback: CallbackQuery, state: FSMContext):
    prefix, category = callback.data.split('|')
    await state.set_state(GoodsState.block_input)
    await state.update_data(category=category)
    await callback.message.edit_text("🛍 Оберіть товар",
                                     reply_markup=build_goods_with_price_inl(category))


@user_router.callback_query(Text(startswith="new_order_g"))
async def anon(callback: CallbackQuery, state: FSMContext):
    prefix, goods_name = callback.data.split('|')
    await state.update_data(ordered_goods=goods_name)