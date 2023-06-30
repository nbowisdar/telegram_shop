from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command, Text
from aiogram import F

from config import contacts
from setup import user_router
from src.database.crud.get import get_user_schema_by_id, get_users_orders
from src.database.tables import User
from src.messages import build_users_orders_msg
from src.schemas import per_by_name
from src.telegram.buttons import *
from src.telegram.handlers.fsm_h.user_fsm.address.add_address import AddressState
from src.telegram.handlers.fsm_h.user_fsm.address.update_address import UpdateAddr
from src.telegram.messages.user_msg import build_address_msg
from src.telegram.utils.check_msg_size import divide_big_msg


@user_router.message(F.text.in_(['/start', "↩️ На головну"]))
async def start(message: Message, state: FSMContext):

    current_state = await state.get_state()
    if current_state:
        await state.clear()

    if not message.from_user.username:
        await message.answer("Ми зберігаємо ваш username, для швидкого зв'язку з вами\n"
                             "Тож будь ласка спочатку створіть username",
                             reply_markup=user_main_btn)
    else:
        User.get_or_create(user_id=message.from_user.id, username=message.from_user.username)
        await message.answer("Головна сторінка 🌞",
                             reply_markup=user_main_btn)


@user_router.callback_query(Text("user_main"))
async def start(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Головна сторінка 🌞", reply_markup=user_main_btn)





@user_router.message(F.text == "🏠 Додати адрес")
async def show_price(message: Message, state: FSMContext):
    await state.set_state(AddressState.full_name)
    await message.answer("Введіть ваше повне ім'я", reply_markup=cancel_btn)


@user_router.message(F.text == "📞 Контакти")
async def community(message: Message):
    msg = "\n".join(
        ["📞 " + number for number in contacts]
    )
    await message.answer(f"Виберіть потрібний контакт нижче:\n{msg}")


@user_router.message(F.text == "✉️ Зв'язок із адміністрацією")
async def community(message: Message):
    await message.answer(f"Клацніть щоб написати",
                         reply_markup=ask_admin)


@user_router.message(F.text == "💻 Відкрити сайт")
async def community(message: Message):
    await message.answer(f"Клацніть щоб відкрити",
                         reply_markup=open_site_inl)


@user_router.message(F.text == "🕺 Мій профіль")
async def profile(message: Message):
    await message.answer("🕺  профіль", reply_markup=build_profile_kb(message.from_user.id))


@user_router.message(F.text == "🔨 Оновити адрес")
async def addr(message: Message):
    user = get_user_schema_by_id(message.from_user.id)
    addr = build_address_msg(user.address)
    await message.answer(addr, parse_mode="MARKDOWN", reply_markup=addr_inline_fields)


@user_router.callback_query(F.data.in_(["full_name", "mobile_number", "city", "post_number"]))
async def update_addr(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UpdateAddr.new_value)
    await state.update_data(field=callback.data)
    await callback.message.reply("Введіть нове значання:", reply_markup=ReplyKeyboardRemove())
    await callback.answer()
    # await message.answer(addr, parse_mode="MARKDOWN", reply_markup=addr_inline_fields)


@user_router.message(F.text == "📦 Мої замовлення")
async def test(message: Message):
    await message.answer("За який проміжок часу?", reply_markup=get_order_kb(message.from_user.id))


@user_router.callback_query(Text(startswith="select_order"))
async def update_addr(callback: CallbackQuery):
    _, user_id, period_str = callback.data.split("|")
    period = per_by_name[period_str]
    orders = get_users_orders(int(user_id), period)
    msg = build_users_orders_msg(orders)
    msgs_list = divide_big_msg(msg)
    if not msg:
        await callback.message.edit_text("🤷‍♂️ У вас ще немає заказів")
    else:
        for msg in msgs_list:
            await callback.message.answer(msg)

    await callback.answer()



