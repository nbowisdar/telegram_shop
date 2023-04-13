from pprint import pprint

from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from peewee import IntegrityError

from setup import user_router
from src.database.crud.create import create_address
from src.schemas import AddressModel
from src.telegram.buttons import user_main_btn
from src.telegram.utils.NP_api import check_city_np_exist, get_np_address


class AddressState(StatesGroup):
    full_name = State()
    mobile_number = State()
    city = State()
    post_number = State()
    user_id = State()


@user_router.message(F.text.casefold() == "❌ відмінити")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer("Відмінено.", reply_markup=user_main_btn)


@user_router.message(AddressState.full_name)
async def set_name(message: Message, state: FSMContext):
    len_name = len(message.text.split(" "))
    if len_name < 2:
        await message.reply("❌ Повинне бути повне ім'я", reply_markup=user_main_btn)
        await state.clear()
        return
    await state.update_data(full_name=message.text)
    await state.set_state(AddressState.mobile_number)
    await message.answer("Введить свій мобільний телефон в форматі `380673171111`",
                         parse_mode="MARKDOWN",)


@user_router.message(AddressState.mobile_number)
async def set_name(message: Message, state: FSMContext):
    number = message.text
    if not number.isdigit() or len(number) != 12 or not number.startswith("380"):
        await state.clear()
        await message.reply("❌ Не вірний формат!\nНомер має починатися з 380", reply_markup=user_main_btn)
        return

    await state.update_data(mobile_number=message.text)
    await state.set_state(AddressState.city)
    await message.answer("Введіть назву свого міста")


@user_router.message(AddressState.city)
async def set_name(message: Message, state: FSMContext):
    city = message.text
    exists = await check_city_np_exist(city)
    if not exists:
        await message.answer("❌ Такого міста не знайденно", reply_markup=user_main_btn)
        await state.clear()
        return

    await state.update_data(city=city)
    await message.answer("Відправьте номер відділення нової пошти")
    await state.set_state(AddressState.post_number)


@user_router.message(AddressState.post_number)
async def set_name(message: Message, state: FSMContext):
    number = message.text

    if not number.isdigit():
        await message.reply("❌ Не вірний формат!", reply_markup=user_main_btn)
    else:
        data = await state.get_data()
        addr = await get_np_address(data['city'], number)
        if not addr:
            await message.reply("❌ Відділення не знайденно!", reply_markup=user_main_btn)
            await state.clear()
            return

        await state.update_data(post_number=message.text)
        await state.update_data(user_id=message.from_user.id)
        data = await state.get_data()
        data = AddressModel(**data)
        try:
            create_address(data)
            msg = f"✅ Ви додали адрес!\nНомер відділення - *№{number}*\nАддресса - `{addr}`"
        except IntegrityError:
            msg = "🛑 Ви можете додати лише один адрес"
        await message.answer(msg, reply_markup=user_main_btn)
    await state.clear()
