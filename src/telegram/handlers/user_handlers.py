from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, Text
from aiogram import F
from setup import user_router
# from src.database.queries import get_order_by_id
# from src.messages import show_accounts_price, show_order
from src.telegram.buttons import user_main_btn, build_acc_btns, community_btn, cancel_btn
from setup import bot
from src.telegram.handlers.fsm_h.user_fsm.address.add_address import AddressState
# from src.telegram.handlers.fsm_h.user_fsm.create_order import OrdrState


@user_router.message(Command(commands='start'))
async def test(message: Message):
    await message.answer("bot works",
                         reply_markup=user_main_btn)


@user_router.message(F.text == "Цена Аккаунтов💸")
async def show_price(message: Message):
    # msg = show_accounts_price()
    msg = "1"
    await message.answer(msg, reply_markup=user_main_btn)


@user_router.message(F.text == "Додати адрес🏠")
async def show_price(message: Message, state: FSMContext):
    await state.set_state(AddressState.full_name)
    await message.answer("Введіть ваше повне ім'я", reply_markup=cancel_btn)


# @user_router.message(F.text == "Купить аккаунт⚡️")
# async def new_order(message: Message, state: FSMContext):
#     await message.answer("Какой аккаунт хотите приобрести?",
#                          reply_markup=build_acc_btns())
#     await state.set_state(OrdrState.account_name)
#     await state.update_data(user_id=message.from_user.id)


@user_router.message(F.text == "Обратная связь✍️")
async def community(message: Message):
    await message.answer("🦾",
                         reply_markup=community_btn)


# @user_router.message(F.text == "/test")
# async def test(message: Message):
#     order = get_order_by_id(1)
#     msg = show_order(order)
#     await message.answer(msg, parse_mode="MARKDOWN")


@user_router.message(F.text == "Применить промокод🧩")
async def test(message: Message):

    await message.answer("dwa", parse_mode="MARKDOWN")


