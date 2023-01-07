from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import F
from setup import user_router
from src.telegram.buttons import user_main_btn, build_acc_btns
from setup import bot
from src.telegram.handlers.fsm_h.user_fsm.create_order import OrdrState


@user_router.message(Command(commands='start'))
async def test(message: Message):
    await message.answer("bot works",
                         reply_markup=user_main_btn)


@user_router.message(F.text == "Купить аккаунт⚡️")
async def new_order(message: Message, state: FSMContext):
    await message.answer("Какой аккаунт хотите приобрести?",
                         reply_markup=build_acc_btns())
    await state.set_state(OrdrState.account_name)
    await state.update_data(user_id=message.from_user.id)



@user_router.message(F.photo)
async def test(message: Message):
    await message.answer("get photo")
    photo = message.photo
    print(photo)
    print(photo[-1])

#
#
@user_router.message(F.text == "/test")
async def test(message: Message):
    await message.answer("get photo")
    photo = message.photo
    print(type(photo[-1].file_id))
