from setup import order_router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command, Text
from aiogram import F

from src.database.crud.get import get_goods_by_name
from src.telegram.buttons import user_main_btn, build_goods_with_price_inl, categories_inl, ok_goods, build_amount_inl
import decimal
from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from src.telegram.handlers.user_handlers import user_router
from src.telegram.buttons import user_main_btn
from src.telegram.messages.user_msg import build_goods_full_info

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
    msg = await message.answer('Генерація нового замовлення 👇', reply_markup=ReplyKeyboardRemove())
    await msg.delete()
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
    await callback.message.delete()

    goods = get_goods_by_name(goods_name)
    msg = build_goods_full_info(goods)
    await callback.message.answer_photo(photo=goods.photo, caption=msg,
                                        reply_markup=ok_goods, parse_mode="MARKDOWN")


# @user_router.callback_query(Text("new_order_amount"))
# async def anon(callback: CallbackQuery, state: FSMContext):
#     await callback.message.answer("Оберіть кількиість за допомогою кнопок.\n"
#                                   "Або просто відправте число",
#                                   reply_markup=build_amount_inl())


async def update_num_text(*, message: Message, name: str, price: int, amount: int, new_msg=False):
    msg = f"Товар:_{name}_ *{amount}* шт. 👉 *{price * amount}* ₴"
    if new_msg:
        await message.answer(msg, parse_mode="MARKDOWN", reply_markup=build_amount_inl())
    else:
        await message.edit_text(msg, parse_mode="MARKDOWN", reply_markup=build_amount_inl())


@user_router.callback_query(Text(startswith="new_order_num"))
async def anon(callback: CallbackQuery, state: FSMContext):
    prefix, action = callback.data.split('|')
    data = await state.get_data()
    amount = data.get("amount", 1)
    name = data['ordered_goods']
    goods = get_goods_by_name(name)

    if action == "finish":
        await callback.message.edit_text(f"Итого: {amount}")
        return
    if action == "start":
        await callback.message.delete()
        await update_num_text(message=callback.message,
                              name=name,
                              amount=amount,
                              price=int(goods.price),
                              new_msg=True)
        return

    if action == "incr":
        amount += 1

    elif action == "decr":
        amount -= 1
    await state.update_data(amount=amount)
    await update_num_text(message=callback.message,
                          name=name,
                          amount=amount,
                          price=int(goods.price))
