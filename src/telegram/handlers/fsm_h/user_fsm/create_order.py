import decimal

from aiogram import F
from aiogram.filters import Text
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

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


@user_router.callback_query(Text("cancel_order"))
async def anon(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer("❌ Скасовано ❌", reply_markup=user_main_btn)


@user_router.message(GoodsState.block_input)
async def new_order(message: Message):
    await message.delete()


# @user_router.callback_query(Text(startswith="new_order_g"))
# async def anon(callback: CallbackQuery, state: FSMContext):
#     prefix, category = callback.data.split('|')
#     await state.update_data(category=category)
#     await callback.message.edit_text("Оберіть товар",
#                                      reply_markup=build_goods_with_price_inl(category))

