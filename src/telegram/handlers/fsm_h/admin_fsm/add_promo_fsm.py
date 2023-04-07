import decimal

from aiogram import F
from aiogram.filters import Text
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from setup import admin_router
from src.database.crud.create import create_goods
from src.database.promo_queries import generate_new_code
from src.schemas import GoodsModel, PromoCodeModel
from src.telegram.buttons import admin_main_kb, build_cat_kb


class PromoCodeState(StatesGroup):
    max_use_left = State()
    discount_percent = State()
    code = State()


@admin_router.message(PromoCodeState.max_use_left)
async def anon(message: Message, state: FSMContext):
    max_use_left = message.text
    if not max_use_left.isdigit():
        await state.clear()
        await message.reply("❌ Повинно бути число!", reply_markup=admin_main_kb)
        return
    await message.answer("Введіть сумму знижки")
    await state.update_data(max_use_left=int(max_use_left))
    await state.set_state(PromoCodeState.discount_percent)


@admin_router.message(PromoCodeState.discount_percent)
async def anon(message: Message, state: FSMContext):
    discount_percent = message.text
    if not discount_percent.isdigit():
        await state.clear()
        await message.reply("❌ Повинно бути число!", reply_markup=admin_main_kb)
        return
    await state.update_data(discount_percent=int(discount_percent))
    data = await state.get_data()
    await state.clear()
    await generate(message, data)


async def generate(message: Message, data: dict):
    code = generate_new_code(max_use_left=data['max_use_left'], discount_percent=data['discount_percent'])
    await message.answer(f"Вітаємо!\nВи створили новий промокод - `{code.code}`\n"
                         f"Можно використати - *{code.max_use_left}* разів\n"
                         f"Надає скидку - *{code.discount_percent}* %",
                         reply_markup=admin_main_kb, parse_mode="MARKDOWN")
