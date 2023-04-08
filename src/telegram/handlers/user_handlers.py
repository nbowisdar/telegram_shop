from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command, Text
from aiogram import F
from setup import user_router
from src.database.crud.get import get_user_schema_by_id
from src.telegram.buttons import user_main_btn, community_btn, cancel_btn, build_profile_kb, \
    addr_inline_fields
from src.telegram.handlers.fsm_h.user_fsm.address.add_address import AddressState
from src.telegram.handlers.fsm_h.user_fsm.address.update_address import UpdateAddr
from src.telegram.messages.user_msg import build_address_msg


@user_router.message(F.text.in_(['/start', "↩️ На головну"]))
async def start(message: Message):
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



@user_router.message(F.text == "✍️ Зворотній зв'язок")
async def community(message: Message):
    await message.answer("🦾",
                         reply_markup=community_btn)


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


# @user_router.message(F.text == "/test")
# async def test(message: Message):
#     bot.his
#     await message.answer(msg, parse_mode="MARKDOWN")


# @user_router.message(F.text == "🧩 Застосувати промокод")
# async def test(message: Message):
#
#     await message.answer("dwa", parse_mode="MARKDOWN")


