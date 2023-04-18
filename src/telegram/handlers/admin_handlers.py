import re
from datetime import datetime, timedelta

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Text
from aiogram import F

from src.database.crud.get import reset_goods_cache, get_order_by_id, get_new_users_by_per, get_all_users_stat, \
    find_user_by, get_last_orders
from src.database.crud.update import update_order_status
from src.database.promo_queries import generate_new_code
from src.database.tables import Goods, Order
from src.messages import build_goods_full_msg, build_order_info_for_admin, build_users_orders_msg
from src.schemas import GoodsModel, per_by_name
from src.telegram.buttons import admin_main_kb, admin_goods_kb, admin_cancel_btn, categories_inl, \
    build_goods_with_price_inl, delete_or_update_one, update_goods_inl, other_bot_btn, find_order_option, \
    update_status_order_choice, update_status_order_inl, new_users_select_per_inl, action_with_found_user
from setup import admin_router, change_status_bot, change_status_pay_card
from setup import bot
from src.telegram.handlers.fsm_h.admin_fsm.add_promo_fsm import PromoCodeState
from src.telegram.handlers.fsm_h.admin_fsm.goods.add_goods import GoodsState
from src.telegram.handlers.fsm_h.admin_fsm.goods.update_goods import GoodsUpdateState
from src.telegram.messages.admin_msg import build_all_new_users_stat_msg, build_info_about_user, build_all_orders_msg
from src.telegram.middleware.check_bot_online import block_user, unblock_user
from src.telegram.utils.check_msg_size import divide_big_msg
from src.telegram.utils.nitifications import send_to_all_users


@admin_router.message(F.text.in_(["/admin", "⬅️ На головну"]))
async def main(message: Message):
    await message.answer("Ти адмін!",
                         reply_markup=admin_main_kb)


@admin_router.callback_query(Text(startswith="admin_drop_msg"))
async def update_goods(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await callback.message.answer("🎉 Головна сторінка", reply_markup=admin_main_kb)


@admin_router.message(F.text == '🛍 Товари')
async def create_promo(message: Message):
    await message.reply(f'Розділ: Товари', reply_markup=admin_goods_kb, parse_mode="MARKDOWN")


@admin_router.message(F.text == "✏️ Додати")
async def add_goods(message: Message, state: FSMContext):
    await message.answer("Введіть назву товару", reply_markup=admin_cancel_btn)
    await state.set_state(GoodsState.name)


@admin_router.message(F.text == "🔨 Оновити")
async def add_goods(message: Message, state: FSMContext):
    await message.delete()
    await message.answer("Оберіть категорію", reply_markup=categories_inl("update_goods_cat", admin=True))


@admin_router.callback_query(Text(startswith="update_goods_cat"))
async def update_goods(callback: CallbackQuery, ):
    _, action = callback.data.split("|")
    await callback.message.edit_text("Оберіть товар, який хочете оновити або видалити",
                                     reply_markup=build_goods_with_price_inl(action,
                                                                             "update_one_goods",
                                                                             True))


@admin_router.callback_query(Text(startswith="update_one_goods"))
async def update_goods(callback: CallbackQuery, state: FSMContext):
    _, id = callback.data.split("|")
    await callback.message.edit_text("Оберіть товар, який хочете оновити або видалити",
                                     reply_markup=delete_or_update_one(id))


@admin_router.callback_query(Text(startswith="change_one"))
async def update_goods(callback: CallbackQuery, state: FSMContext):
    _, action, goods_id = callback.data.split("|")
    goods = Goods.get(id=goods_id)
    if action == "delete":
        reset_goods_cache()
        goods.delete_instance()
        await callback.message.edit_text("🗑 Товар видаленно")

    elif action == "update":
        await state.set_state(GoodsUpdateState.field)
        goods_model = GoodsModel.from_orm(goods)

        await state.update_data(goods=goods_model)
        msg = build_goods_full_msg(goods_model)
        await callback.message.delete()
        await callback.message.answer_photo(photo=goods.photo, caption=msg,
                                            parse_mode="MARKDOWN",
                                            reply_markup=update_goods_inl(goods_model))



@admin_router.message(F.text == "🔑 Створити новий промокод")
async def new_code(message: Message, state: FSMContext):
    await state.set_state(PromoCodeState.max_use_left)
    await message.answer("Введіть число, скільки разів можно використати цей промокод",
                         reply_markup=ReplyKeyboardRemove())


@admin_router.callback_query(Text(startswith="order_waiting"))
async def get_new_order(callback: CallbackQuery):
    _, action = callback.data.split("|")
    pattern = r"Id - (\d+)"
    match = re.search(pattern, callback.message.text)
    user_id = match.group(1)
    order_id = re.search("№ (\d+)", callback.message.text).group(1)

    if action == "confirm":
        msg = "✅ Підтвердженно"
        ans = "✅ Ваше замовлення підтверджено!\n"
        update_order_status(order_id, "confirmed")

    else:
        ans = "❌ Ваше замовлення було відхилено\n" \
              "Якщо у вас залишилися питання" \
              " ви можете звернутися до нашої підтримку."
        msg = "❌ Відхилено"
        update_order_status(order_id, "canceled")

    await callback.message.edit_text(msg)
    await bot.send_message(user_id, ans)
    await callback.answer()


@admin_router.message(F.text == "💾 Інше")
async def anon(message: Message, state: FSMContext):
    await message.answer("Інші функції",
                         reply_markup=other_bot_btn())


@admin_router.message(F.text.in_(["🛑 Зупинити бота", "🚀 Запустити бота"]))
async def anon(message: Message, state: FSMContext):
    change_status_bot()
    if message.text == "🛑 Зупинити бота":
        await message.answer("⏸ Роботу бота зупиненно!", reply_markup=other_bot_btn())
    else:
        await message.answer("🎉 Бот активованно!", reply_markup=other_bot_btn())


@admin_router.message(F.text.in_(["⚠️ Призупинити оплату 💳", "♻️ Поновити оплату 💳"]))
async def anon(message: Message, state: FSMContext):
    change_status_pay_card()
    if message.text == "⚠️ Призупинити оплату 💳":
        await message.answer("⏸ Прийом оплати на карту зупиненно!", reply_markup=other_bot_btn())
    else:
        await message.answer("🎉 Прийом платежів на карту активовано!", reply_markup=other_bot_btn())


class NotifyAll(StatesGroup):
    msg = State()


@admin_router.message(F.text == "📫 Розіслати повідомлення")
async def anon(message: Message, state: FSMContext):
    await state.set_state(NotifyAll.msg)
    await message.answer("Надішли мені повідомлення котре отримують усі користувачи.", reply_markup=admin_cancel_btn)


@admin_router.message(NotifyAll.msg)
async def anon(message: Message, state: FSMContext):
    await send_to_all_users(message)
    await state.clear()


class FindOrder(StatesGroup):
    order_id = State()
    cur_msg = State()


@admin_router.message(F.text == "📊 Замовлення")
async def anon(message: Message):
    await message.answer("🛍 Замовлення", reply_markup=find_order_option)


@admin_router.message(F.text == "🔍 Знайти замовлення")
async def anon(message: Message, state: FSMContext):
    await message.answer("Відправте id замовлення", reply_markup=admin_cancel_btn)
    await state.set_state(FindOrder.order_id)


@admin_router.message(FindOrder.order_id)
async def anon(message: Message, state: FSMContext):

    order_id = message.text
    if not order_id.isdigit():
        await message.reply("❌ Повинно бути число", reply_markup=find_order_option)
        await state.clear()
        return
    order = get_order_by_id(int(order_id))
    if order:
        msg = build_order_info_for_admin(order)
        cur_msg = await message.answer(msg, reply_markup=update_status_order_inl(order_id))
        await state.update_data(cur_msg=cur_msg)
    else:
        msg = "⚠️ Замовлення не знайдено"
        await state.clear()
        await message.reply(msg, reply_markup=find_order_option)


@admin_router.callback_query(Text("to_main_admin_drop_msg"))
async def anon(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    else:
        await state.clear()

    await callback.message.delete()
    await callback.message.answer("Головна", reply_markup=admin_main_kb)


@admin_router.callback_query(Text(startswith='update_order_status|'))
async def anon(callback: CallbackQuery, state: FSMContext):
    # _, order_id, new_status = callback.data.split("|")
    _, order_id = callback.data.split("|")

    data = await state.get_data()
    await data['cur_msg'].edit_text("Оберіть новий статус",
                                    reply_markup=update_status_order_choice(int(order_id)))


@admin_router.callback_query(Text(startswith='update_order_choice|'))
async def anon(callback: CallbackQuery, state: FSMContext):
    _, order_id, new_status = callback.data.split("|")
    # print(new_status)
    update_order_status(int(order_id), new_status)
    order = get_order_by_id(int(order_id))
    msg = build_order_info_for_admin(order)
    await callback.message.edit_text(msg, reply_markup=update_status_order_inl(order_id))


class FindUser(StatesGroup):
    user_id_or_username = State()
    cur_msg = State()


@admin_router.message(F.text == "🔍 Знайти користувача")
async def find_user(message: Message, state: FSMContext):
    await message.answer("Відправте id або username", reply_markup=admin_cancel_btn)
    await state.set_state(FindUser.user_id_or_username)


@admin_router.message(FindUser.user_id_or_username)
async def anon(message: Message, state: FSMContext):

    user = find_user_by(message.text)
    if user:
        msg = build_info_about_user(user)
        await message.answer(msg, reply_markup=action_with_found_user(user.user_id))
    else:
        msg = "⚠️ Користувача не знайдено"
        await message.reply(msg, reply_markup=find_order_option)

    await state.clear()


@admin_router.callback_query(Text(startswith='found_user|'))
async def anon(callback: CallbackQuery, state: FSMContext):
    prefix, action, user_id = callback.data.split('|')
    user_id = int(user_id)
    if action == "last_10_order":
        orders = get_last_orders(user_id, 10)
        if orders:
            msg = build_users_orders_msg(orders)
            msgs_list = divide_big_msg(msg)
            for msg in msgs_list:
                await callback.message.answer(msg, reply_markup=admin_main_kb)
        else:
            await callback.message.answer("Немає замовлень", reply_markup=admin_main_kb)
        await callback.message.delete()


    else:
        if action == "unblock":
            unblock_user(user_id)
        elif action == "block":
            block_user(user_id)

        await callback.message.edit_reply_markup(reply_markup=action_with_found_user(user_id))


class GetOrders(StatesGroup):
    date = State()


@admin_router.message(F.text == "📙 Усі замовлення")
async def find_user(message: Message, state: FSMContext):
    await message.answer("Укажіть проміжок часу у днях", reply_markup=admin_cancel_btn)
    await state.set_state(GetOrders.date)


@admin_router.message(GetOrders.date)
async def anon(message: Message, state: FSMContext):
    d = message.text
    if not d.isdigit():
        await message.reply("Повинне бути число!", reply_markup=admin_main_kb)
        await state.clear()
        return
    delta = datetime.now() - timedelta(days=int(d))
    print(delta)
    orders = Order.select().where(Order.time_created > delta)
    msg = build_all_orders_msg(orders)
    if not msg:
        return await message.answer("🤷‍♂️ За цей проміжк часу немає замовлнь",
                                    reply_markup=find_order_option)
    else:
        for msg in divide_big_msg(msg):
            await message.answer(msg, reply_markup=find_order_option)
    await state.clear()


@admin_router.message(F.text == "📈 Статистика")
async def anon(message: Message):
    await message.answer("🙋‍♂️ Нових юзерів:", reply_markup=new_users_select_per_inl)


@admin_router.callback_query(Text(startswith='new_user_stat|'))
async def anon(callback: CallbackQuery):
    _, period_str = callback.data.split("|")
    if period_str == "all_new_user_stat":
        stat = get_all_users_stat()
        msg = build_all_new_users_stat_msg(stat)
        await callback.message.edit_text(msg)
        return
    period = per_by_name[period_str]
    users_amount = get_new_users_by_per(period)
    await callback.message.edit_text(f"👨‍🔧 Нових користувачів: *{users_amount}*")
