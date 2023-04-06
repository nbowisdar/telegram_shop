from pprint import pprint

from config import card
from setup import order_router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command, Text
from aiogram import F

from src.database.crud.get import get_goods_by_name, get_user_schema_by_id
from src.database.queries import check_promo
from src.schemas import AddressModel, OrderModel
from src.telegram.buttons import *
import decimal
from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from src.telegram.handlers.fsm_h.user_fsm.address.add_address import AddressState
# from src.telegram.handlers.user_handlers import order_router
from src.telegram.buttons import user_main_btn
from src.telegram.messages.user_msg import build_goods_full_info, build_address_msg, build_result_order_msg

"""
class OrderModel(NamedTuple):
    time_created: datetime
    ordered_goods: GoodsModel
    amount: int
    user: UserModel
    with_discount: bool
    note: str | None = None
"""


class OrderState(StatesGroup):
    goods_name = State()
    amount = State()
    user_id = State()
    with_discount = State()
    note = State()
    block_input = State()
    current_msg = State()
    payment = State()


@order_router.message(OrderState.block_input)
async def new_order(message: Message):
    await message.delete()


@order_router.message(F.text == "🛒 Обрати товар")
async def new_order(message: Message, state: FSMContext):
    await state.set_state(OrderState.block_input)
    data = await state.get_data()
    # print(data)
    await state.update_data(user_id=(data.get("user_id", message.from_user.id)))
    msg = await message.answer('Генерація нового замовлення 👇', reply_markup=ReplyKeyboardRemove())
    # data = await state.get_data()
    # print(data)

    await msg.delete()
    await message.answer("Оберіть категорію", reply_markup=categories_inl())


@order_router.callback_query(Text(startswith="order_drop"))
async def anon(callback: CallbackQuery, state: FSMContext):
    _, action = callback.data.split("|")
    await callback.message.delete()
    if action == "cancel":
        await state.clear()
        await callback.message.answer("❌ Скасовано ❌", reply_markup=user_main_btn)
        return
    await new_order(callback.message, state)


@order_router.callback_query(Text(startswith="new_order_cat"))
async def anon(callback: CallbackQuery, state: FSMContext):
    prefix, category = callback.data.split('|')
    await state.set_state(OrderState.block_input)
    await state.update_data(category=category)
    await callback.message.edit_text("🛍 Оберіть товар",
                                     reply_markup=build_goods_with_price_inl(category))


@order_router.callback_query(Text(startswith="new_order_g"))
async def anon(callback: CallbackQuery, state: FSMContext):
    prefix, goods_name = callback.data.split('|')
    await state.update_data(goods_name=goods_name)
    await callback.message.delete()

    goods = get_goods_by_name(goods_name)
    msg = build_goods_full_info(goods)
    await callback.message.answer_photo(photo=goods.photo, caption=msg,
                                        reply_markup=ok_goods, parse_mode="MARKDOWN")




async def update_num_text(*, message: Message, name: str, price: int, amount: int, new_msg=False):
    msg = f"Товар:_{name}_ *{amount}* шт. 👉 *{price * amount}* ₴"
    if new_msg:
        await message.answer(msg, parse_mode="MARKDOWN", reply_markup=build_amount_inl())
    else:
        await message.edit_text(msg, parse_mode="MARKDOWN", reply_markup=build_amount_inl())


@order_router.callback_query(Text(startswith="new_order_num"))
async def anon(callback: CallbackQuery, state: FSMContext):

    prefix, action = callback.data.split('|')
    data = await state.get_data()

    amount = data.get("amount", 1)
    name = data['goods_name']
    goods = get_goods_by_name(name)

    if action == "finish":
        await select_address(callback, state)
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


@order_router.callback_query(Text(startswith="new_order_addr"))
async def select_address(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user = get_user_schema_by_id(data['user_id'])
    if user.address:
        msg = "Бажаєте викорастити цей адрес?\n\n" + build_address_msg(user.address)
        await callback.message.edit_text(msg, parse_mode="MARKDOWN",
                                         reply_markup=build_addr_inl())
    else:
        await state.clear()
        msg = "Будьласка, спочатку додайте ваш адрес."
        # await callback.message.edit_text(msg)
        await callback.message.delete()
        await state.set_state(AddressState.full_name)
        await callback.message.answer(msg+"\n\nВведіть ваше повне ім'я", reply_markup=cancel_btn)
    # prefix, category = callback.data.split('|')
    # await state.set_state(OrderState.block_input)
    # await state.update_data(category=category)
    # await callback.message.edit_text("🛍 Оберіть товар",
    #                                  reply_markup=build_goods_with_price_inl(category))


# TODO: can be better with choosing address
@order_router.callback_query(Text("update_addr"))
async def anon(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    msg = "Заказ скасовано, після оновлення вашого адресу будьласка відтворити свої дії."
    await callback.message.edit_text(msg)
    user = get_user_schema_by_id(callback.from_user.id)
    addr = build_address_msg(user.address)
    await callback.message.answer(addr, parse_mode="MARKDOWN", reply_markup=addr_inline_fields)


@order_router.callback_query(Text("addr_confirmed"))
async def anon(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("У вас є промокод?", reply_markup=if_promo_inl)



@order_router.callback_query(Text("try_discount"))
async def anon(callback: CallbackQuery, state: FSMContext):
    await state.update_data(current_msg=callback.message)
    await callback.message.edit_text("Відправте промокод ✍️")
    await state.set_state(OrderState.with_discount)


@order_router.message(OrderState.with_discount)
async def anon(message: Message, state: FSMContext):
    code = check_promo(message.text)
    await message.delete()
    data = await state.get_data()
    msg: Message = data["current_msg"]
    if code:
        await msg.edit_text("✅ Вітаємо, ви додали промоко!",
                            reply_markup=create_new_ordr_inl)
    else:
        await msg.edit_text(f"{msg.text}\n\n❌ Код не дійсний!",
                            parse_mode="MARKDOWN", reply_markup=if_promo_inl)


@order_router.callback_query(Text("show_oder_details"))
async def show_order_details(callback: CallbackQuery, state: FSMContext):
    user = get_user_schema_by_id(callback.from_user.id)
    data = await state.get_data()
    goods = get_goods_by_name(data['goods_name'])
    amount = data.get("amount", 1)
    order = OrderModel(user=user, amount=amount, ordered_goods=goods)
    msg = build_result_order_msg(order, user.address)
    await state.update_data(payment=order.amount*order.ordered_goods.price)
    await callback.message.edit_text(msg, parse_mode="MARKDOWN", reply_markup=create_new_ordr_inl)


@order_router.callback_query(Text("confirm_order"))
async def anon(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    # create_new_order()

    msg = f"Вітаємо, ви створили нове замовлення!\n" \
          f"Будь ласка здейсніть оплату.\n" \
          f"На карту `{card}`\n" \
          f"У розмірі - `{data['payment']}` ₴\n" \
          f"Після чого натисніть - *Оплатив*"
    await callback.message.edit_text(msg, reply_markup=pay_inl, parse_mode="MARKDOWN")


@order_router.callback_query(Text("confirm_pay"))
async def anon(callback: CallbackQuery, state: FSMContext):
    # data = await state.get_data()
    # await send_confirmation_to_admin()
    msg = "Дякуємо за замовлення." \
          "Усю інформацію по вашому заказу буде перевіренно" \
          "Та після перевірки оплати товар буде ваи відправленно." \
          "Якщо залишилися питання, ви завжди можете написати нам перший." \
          "П.с Впевніться що вам можуть писати першими (якщо з являться уточнення з нашої сторони)"
    msg_anon = await callback.message.answer("🌞", reply_markup=user_main_btn)
    await callback.message.edit_text(msg)
