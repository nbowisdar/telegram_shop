from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from setup import user_router


class OrdrState(FSMContext):
    user_id = State()
    account_name = State()
    city = State()
    sex = State()
    with_discount = State()
    selfie = State()
    car = State()
    note = State()


@user_router.message(OrdrState.account_name)
async def set_acc_name(message: Message, state: FSMContext):
    await state.update_data(account_name=message.text)
    await state.set_state(OrdrState.city)
    await message.reply("Введите свой город.")


@user_router.message(OrdrState.city)
async def set_acc_name(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await state.set_state(OrdrState.sex)
    await message.reply("Введите свой пол.")


@user_router.message(OrdrState.sex)
async def set_acc_name(message: Message, state: FSMContext):
    await state.update_data(sex=message.text)
    await state.set_state(OrdrState.with_discount)
    await message.reply("Введите промокод (если есть).",
                        reply_markup=ReplyKeyboardMarkup(
                            keyboard=[[KeyboardButton(text="У меня нет промокода")]],
                            resize_keyboard=True
                        ))


@user_router.message(OrdrState.with_discount)
async def set_acc_name(message: Message, state: FSMContext):
    await state.update_data(with_discount=message.text)
    await state.set_state(OrdrState.selfie)
    await message.reply("Отправте свое селфи.")


@user_router.message(OrdrState.selfie)
async def set_acc_name(message: Message, state: FSMContext):
    await state.update_data(selfie=message.text)
    await state.set_state(OrdrState.car)
    await message.reply("Отправте свое селфи.")


@user_router.message(OrdrState.selfie)
async def set_acc_name(message: Message, state: FSMContext):
    await state.update_data(selfie=message.text)
    await state.set_state(OrdrState.car)
    await message.reply("Какой у вас автомобиль (год, марка, модель, цвет)?")


@user_router.message(OrdrState.car)
async def set_acc_name(message: Message, state: FSMContext):
    await state.update_data(car=message.text)
    await state.set_state(OrdrState.note)
    await message.reply("Хотите добавить коментарий к заказу?")


@user_router.message(OrdrState.note)
async def set_acc_name(message: Message, state: FSMContext):
    await state.update_data(note=message.text)
    data = await state.get_data()
    await state.clear()
    save_order(data)


def save_order(data: dict):
    pass