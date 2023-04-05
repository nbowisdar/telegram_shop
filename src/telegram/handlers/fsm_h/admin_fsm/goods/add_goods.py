import decimal

from aiogram import F
from aiogram.filters import Text
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from setup import admin_router
from src.database.crud.create import create_goods
from src.schemas import GoodsModel
from src.telegram.buttons import admin_main_kb, build_cat_kb

"""
class GoodsModel(TypedDict):
    name: str
    desc: str
    price: decimal.Decimal
    photo: str
"""


class GoodsState(StatesGroup):
    name = State()
    desc = State()
    category = State()
    price = State()
    photo = State()


@admin_router.message(F.text.casefold() == "🛑 відмінити")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer("Відмінено.", reply_markup=admin_main_kb)


@admin_router.message(GoodsState.name)
async def set_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(GoodsState.desc)
    await message.answer("Введить опис до товару",
                         parse_mode="MARKDOWN",)


@admin_router.message(GoodsState.desc)
async def set_name(message: Message, state: FSMContext):
    await state.update_data(desc=message.text)
    # await state.set_state(GoodsState.category)
    await message.answer("Оберіть категорію", reply_markup=build_cat_kb(is_admin=True))


@admin_router.callback_query(Text(startswith="add_goods|"))
async def add_state(callback: CallbackQuery, state: FSMContext):
    prefix, category = callback.data.split('|')
    await state.update_data(category=category.casefold())
    await state.set_state(GoodsState.price)
    await callback.message.edit_text("Укажіть ціну")


@admin_router.message(GoodsState.price)
async def set_name(message: Message, state: FSMContext):
    try:
        price = decimal.Decimal(message.text)
        await state.update_data(price=price.quantize(decimal.Decimal("0.01")))
    except (decimal.InvalidOperation, TypeError):
        await state.clear()
        await message.reply("❌ Не вірне значення!", reply_markup=admin_main_kb)
        return

    await message.answer("Відправте фото товара")
    await state.set_state(GoodsState.photo)


@admin_router.message(GoodsState.photo)
async def set_name(message: Message, state: FSMContext):
    try:
        await state.update_data(photo=message.photo[-1].file_id)
        await message.delete()
        data = await state.get_data()
        created = create_goods(GoodsModel(**data))
        if created:
            await message.answer("✅ Ви додали новий товар!", reply_markup=admin_main_kb)
        else:
            await message.answer("❌ Помилка\nСкорішь за все такий товар вже існує!", reply_markup=admin_main_kb)

    except TypeError:
        await message.reply("❌ Ви повинні відправити фото!",
                            reply_markup=admin_main_kb)
    finally:
        await state.clear()


