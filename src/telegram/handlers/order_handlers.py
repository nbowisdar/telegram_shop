from pprint import pprint

from config import card, buy_variants
from setup import order_router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command, Text
from aiogram import F

from src.database.crud.create import create_new_order
from src.database.crud.get import get_goods_by_name, get_user_schema_by_id
from src.database.promo_queries import apply_promo_code
from src.database.tables import order_status, type_payment, Order, buy_variants_struct, Goods
from src.schemas import AddressModel, OrderModel, AmountPrice
from src.telegram.buttons import *
import decimal
from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from src.telegram.handlers.fsm_h.user_fsm.address.add_address import AddressState
# from src.telegram.handlers.user_handlers import order_router
from src.telegram.buttons import user_main_btn
from src.telegram.messages.user_msg import build_goods_full_info, build_address_msg, build_result_order_msg, \
    build_msg_discount_amount
from src.telegram.utils.nitifications import send_confirmation_to_admin


class OrderState(StatesGroup):
    goods_name = State()
    amount_disc = State()
    user_id = State()
    username = State()
    with_discount = State()
    note = State()
    promo_code = State()
    block_input = State()
    current_msg = State()
    total = State()
    discount = State()
    order_msg = State()
    type_payment = State()


@order_router.message(OrderState.block_input)
async def new_order(message: Message):
    await message.delete()


@order_router.message(F.text == "🛒 Обрати товар")
async def new_order(message: Message, state: FSMContext):
    await state.set_state(OrderState.block_input)
    data = await state.get_data()
    # await state.update_data(amount_disc=buy_variants_struct[0])
    await state.update_data(discount=0)
    await state.update_data(user_id=(data.get("user_id", message.from_user.id)))
    await state.update_data(username=(data.get("username", message.from_user.username)))
    msg = await message.answer('Генерація нового замовлення 👇', reply_markup=ReplyKeyboardRemove())

    await msg.delete()
    await message.answer("Оберіть категорію", reply_markup=categories_inl(admin=False))


@order_router.callback_query(Text(startswith="order_drop"))
async def anon(callback: CallbackQuery, state: FSMContext):
    _, action = callback.data.split("|")
    await callback.message.delete()
    if action == "cancel":
        await state.clear()
        await callback.message.answer("❌ Скасовано ❌", reply_markup=user_main_btn)
        return
    await callback.message.answer("Оберіть категорію", reply_markup=categories_inl(admin=False))
    # await new_order(callback.message, state)


@order_router.callback_query(Text(startswith="new_order_cat"))
async def anon(callback: CallbackQuery, state: FSMContext):
    prefix, category = callback.data.split('|')
    await state.set_state(OrderState.block_input)
    await state.update_data(category=category)

    await callback.message.edit_text("🛍 Оберіть товар",
                                     reply_markup=build_goods_with_price_inl(category))


@order_router.callback_query(Text(startswith="new_order_g"))
async def anon(callback: CallbackQuery, state: FSMContext):
    prefix, goods_id_or_desc, = callback.data.split('|')
    if goods_id_or_desc == "description":
        data = await state.get_data()
        goods_name = data["goods_name"]
    else:
        goods_name = Goods.get_by_id(int(goods_id_or_desc)).name
        await state.update_data(goods_name=goods_name)
        await callback.message.delete()
    goods = get_goods_by_name(goods_name)
    price = float(goods.price)
    if goods_id_or_desc == "description":
        msg = build_msg_discount_amount(goods, buy_variants, with_desc=True)
        with_desc_btn = False
        await callback.message.edit_caption(caption=msg,
                                            reply_markup=build_amount_disc_inl(price, with_desc_btn))

    else:
        with_desc_btn = True
        msg = build_msg_discount_amount(goods, buy_variants)
        await callback.message.answer_photo(photo=goods.photo, caption=msg,
                                            reply_markup=build_amount_disc_inl(price, with_desc_btn))


@order_router.callback_query(Text(startswith="new_order_addr"))
async def select_address(callback: CallbackQuery, state: FSMContext):

    _, n = callback.data.split("|")
    await state.update_data(amount_disc=buy_variants_struct[int(n)])

    data = await state.get_data()
    user = get_user_schema_by_id(data['user_id'])

    if isinstance(callback, Message):
        if user.address:
            # print(callback)
            # print(callback.text)
            msg = "Бажаєте викорастити цей адрес?\n\n" + build_address_msg(user.address)
            await callback.edit_text(msg, parse_mode="MARKDOWN",
                                             reply_markup=build_addr_inl())
        else:
            await state.clear()
            msg = "Будьласка, спочатку додайте ваш адрес."
            # await callback.edit_text(msg)
            await callback.delete()
            await state.set_state(AddressState.full_name)
            await callback.answer(msg+"\n\nВведіть ваше повне ім'я", reply_markup=cancel_btn)
    else:
        await callback.message.delete()
        if user.address:
            msg = "Бажаєте викорастити цей адрес?\n\n" + build_address_msg(user.address)
            await callback.message.answer(msg, parse_mode="MARKDOWN",
                                             reply_markup=build_addr_inl())
        else:
            await state.clear()
            msg = "Будьласка, спочатку додайте ваш адрес."
            await state.set_state(AddressState.full_name)
            await callback.message.answer(msg + "\n\nВведіть ваше повне ім'я", reply_markup=cancel_btn)


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
async def has_promo(callback: CallbackQuery, state: FSMContext):
    await state.update_data(current_msg=callback.message)
    await callback.message.edit_text("У вас є промокод?", reply_markup=if_promo_inl)


@order_router.callback_query(Text("try_discount"))
async def anon(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Відправте промокод ✍️")
    await state.set_state(OrderState.with_discount)


@order_router.message(OrderState.with_discount)
async def anon(message: Message, state: FSMContext):
    try:
        code = apply_promo_code(message.text, message.from_user.id)
    except Exception as err:
        data = await state.get_data()
        await message.reply(str(err))
        await data['current_msg'].answer("У вас є промокод?", reply_markup=if_promo_inl)
        return
    await message.delete()
    data = await state.get_data()
    msg: Message = data["current_msg"]
    if code:
        await state.update_data(promo_code=code)
        await state.update_data(discount=code.discount_percent)
        await msg.answer("✅ Вітаємо, ви додали промокод!\n"
                            f"      Діє знижка -{code.discount_percent} %\n\n")

        await choose_payment(msg)

    else:
        await msg.edit_text(f"{msg.text}\n\n❌ Код не дійсний!",
                            parse_mode="MARKDOWN", reply_markup=if_promo_inl)


@order_router.callback_query(Text("type_payment"))
async def choose_payment(obj):
    if isinstance(obj, Message):
        await obj.edit_text("Оберіть тип оплати", reply_markup=type_delivery_inl)
    else:
        await obj.message.edit_text("Оберіть тип доставки", reply_markup=type_delivery_inl)



@order_router.callback_query(Text(startswith="payment"))
async def anon(callback: CallbackQuery, state: FSMContext):
    _, key = callback.data.split("|")

    await state.update_data(type_payment=key)
    await callback.message.edit_text(f"Тип оплати - *{type_payment[key]}*",
                                     parse_mode="MARKDOWN",
                                     reply_markup=show_details)


@order_router.callback_query(Text("show_oder_details"))
async def show_order_details(callback: CallbackQuery, state: FSMContext):
    user = get_user_schema_by_id(callback.from_user.id)
    data = await state.get_data()
    goods = get_goods_by_name(data['goods_name'])
    amount_disc = data.get("amount_disc", buy_variants_struct[0])
    # print(amount_disc, 305)
    order = OrderModel(user_id=user.user_id,
                       amount_disc=amount_disc,
                       ordered_goods=goods,
                       total=0,
                       type_payment=type_payment.get(
                           data['type_payment'])
                       )

    total = round(amount_disc.amount * goods.price / 100 * amount_disc.price)
    if 'promo_code' in data.keys():
        # print(data['promo_code'], 276)
        disc_percent = data['promo_code'].discount_percent
        total -= round(total / 100 * disc_percent)
        order.total = total
        order.discount = disc_percent

    msg = build_result_order_msg(order, user.address, float(total))
    await state.update_data(order_msg=msg)

    await state.update_data(total=total)
    await callback.message.edit_text(msg, parse_mode="MARKDOWN", reply_markup=create_new_ordr_inl)


@order_router.callback_query(Text("confirm_order"))
async def anon(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    # await state.update_data(order=order)
    # print(data['type_payment'])

    if data['type_payment'] == "now":  # if user choose to pay online
        msg = f"Вітаємо, ви створили нове замовлення!\n" \
              f"Будь ласка здейсніть оплату.\n" \
              f"На карту `{card}`\n" \
              f"У розмірі - `{data['total']}` ₴\n" \
              f"Після чого натисніть - *Оплатив*"
        await callback.message.edit_text(msg, reply_markup=pay_inl, parse_mode="MARKDOWN")
    else:
        await confirm_payment(callback, state)


@order_router.callback_query(Text("confirm_pay"))
async def confirm_payment(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    amount_disc = data.get("amount_disc", buy_variants_struct[0])
    data['amount'] = amount_disc.amount
    order: Order = create_new_order(data)
    order.status = "wait_confirmation"
    order.save()
    data['order_id'] = order.id
    await notify_admins(data)

    msg = "Дякуємо!\n" \
          f"Номер вашого замовлення - `{order.id}`\n\n" \
          "Усю інформацію по вашому заказу буде перевіренно" \
          "Якщо залишилися питання, ви завжди можете написати нам перший." \
          "П.с Переконайтеся що вам можуть писати першими (якщо з'являться уточнення з нашої сторони)"
    await callback.message.answer("🌞🚀", reply_markup=user_main_btn, )
    await callback.message.edit_text(msg, parse_mode="MARKDOWN")
    await state.clear()

    if "promo_code" in data.keys():
        apply_promo_code(data['promo_code'].code, data['user_id'], True)


async def notify_admins(data: dict):
    msg_for_admin = f"Нове замовлення - № `{data['order_id']}`\n" \
                    f"Юзер - `{data['username']}`\nId - `{data['user_id']}`" \
                    f"\n\n{data['order_msg']}\n" \
                    f"Статус - *{order_status['wait_confirmation']}*"
    await send_confirmation_to_admin(msg_for_admin)

