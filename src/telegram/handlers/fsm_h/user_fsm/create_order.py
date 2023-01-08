from pprint import pprint

from aiogram import F
from aiogram.filters import Command

from src.messages import show_order
from src.other import send_new_order_to_admin
from src.telegram.buttons import user_main_btn, cancel_btn, sex_btn
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from setup import user_router
from src.database.queries import check_promo, create_order, get_account_by_name
from src.schemas import OrderModel


class OrdrState(StatesGroup):
    user_id = State()
    account_name = State()
    account_id = State()
    account_username = State()
    account_price = State()
    city = State()
    sex = State()
    with_discount = State()
    disc_code = State()
    selfie = State()
    car = State()
    note = State()


@user_router.message(F.text == "Отмена")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(
        "Отменено.",
        reply_markup=user_main_btn)


@user_router.message(OrdrState.account_name)
async def set_acc_name(message: Message, state: FSMContext):
    acc = get_account_by_name(message.text)
    await state.update_data(account_name=message.text)
    await state.update_data(account_username=message.from_user.username)

    await state.update_data(account_id=acc.id)
    await state.update_data(account_price=acc.price)
    await state.set_state(OrdrState.city)
    await message.reply("Введите свой город.",
                        reply_markup=cancel_btn)


@user_router.message(OrdrState.city)
async def set_acc_name(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await state.set_state(OrdrState.sex)
    await message.reply("Введите свой пол.",
                        reply_markup=sex_btn)


@user_router.message(OrdrState.sex)
async def set_acc_name(message: Message, state: FSMContext):
    await state.update_data(sex=message.text)
    await state.set_state(OrdrState.with_discount)
    await message.reply("Введите промокод (если есть).",
                        reply_markup=ReplyKeyboardMarkup(
                            keyboard=[[KeyboardButton(text="У меня нет промокода"), KeyboardButton(text="Отмена")]],
                            resize_keyboard=True
                        ))


@user_router.message(OrdrState.with_discount)
async def set_acc_name(message: Message, state: FSMContext):
    try:
        if message.text == "У меня нет промокода":
            disc_code = None
            with_disc = False
        else:
            disc_code = check_promo(message.text)
            with_disc = True
        await state.update_data(with_discount=with_disc)
        await state.update_data(disc_code=disc_code)
        await state.set_state(OrdrState.selfie)
        await message.reply("Отправте свое селфи.",
                            reply_markup=cancel_btn)
    except TypeError:
        await message.reply("Не верный промокод!", reply_markup=user_main_btn)
        await state.clear()
        return


@user_router.message(OrdrState.selfie)
async def set_acc_name(message: Message, state: FSMContext):
    try:
        await state.update_data(selfie=message.photo[-1].file_id)
        await state.set_state(OrdrState.car)
        await message.reply("Какой у вас автомобиль (год, марка, модель, цвет)?",
                            reply_markup=ReplyKeyboardMarkup(
                                keyboard=[[KeyboardButton(text="У меня нет авто"), KeyboardButton(text="Отмена")]],
                                resize_keyboard=True
                            ))
    except TypeError:
        await state.clear()
        await message.reply("Вы должны отправить фото!",
                            reply_markup=user_main_btn)


@user_router.message(OrdrState.car)
async def set_acc_name(message: Message, state: FSMContext):
    if message.text == "У меня нет авто":
        car = None
    else:
        car = message.text
    await state.update_data(car=car)
    await state.set_state(OrdrState.note)
    await message.reply("Хотите добавить коментарий к заказу?",
                        reply_markup=ReplyKeyboardMarkup(
                            keyboard=[[KeyboardButton(text="Нет"), KeyboardButton(text="Отмена")]],
                            resize_keyboard=True
                        ))


@user_router.message(OrdrState.note)
async def set_acc_name(message: Message, state: FSMContext):
    if message.text == "Нет":
        note = None
    else:
        note = message.text
    await state.update_data(note=note)
    data = await state.get_data()
    await state.clear()
    await save_order(message, data)


async def save_order(message: Message, data: dict):
    struct_data = OrderModel(**data)
    create_order(struct_data)
    order_msg = show_order(struct_data)
    # increase the amount of use
    check_promo(name=struct_data.disc_code, incr_amount=True)

    msg = "Вы создали новый заказ!" + order_msg
    await message.answer(msg, reply_markup=user_main_btn, parse_mode="MARKDOWN")

    order_msg = f"Пользователь `{message.from_user.id}` создал новый заказ!\n" + order_msg
    await send_new_order_to_admin(order_msg, struct_data.selfie)
