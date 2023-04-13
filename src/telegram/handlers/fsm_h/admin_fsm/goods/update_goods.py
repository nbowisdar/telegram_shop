from pprint import pprint

from aiogram.fsm.state import State, StatesGroup


from setup import order_router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command, Text

from src.database.crud.update import update_goods_field
from src.messages import build_goods_full_msg
from src.telegram.buttons import *
from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from src.telegram.buttons import user_main_btn


class GoodsUpdateState(StatesGroup):
    goods = State()
    field = State()
    new_value = State()


async def update_goods_category(message: Message, state: FSMContext):
    await message.edit_text("Оберіть категорію", reply_markup=categories_inl())


@order_router.callback_query(Text(startswith="admin_drop_msg"))
async def anon(callback: CallbackQuery, state: FSMContext):
    _, action = callback.data.split("|")
    await callback.message.delete()
    if action == "cancel":
        await callback.message.answer("❌ Скасовано ❌", reply_markup=admin_main_kb)
        await state.clear()
        return

    # await new_order(callback.message, state)


@order_router.callback_query(Text(startswith="update_goods_field"))
async def anon(callback: CallbackQuery, state: FSMContext):
    prefix, field = callback.data.split('|')
    await state.update_data(field=field)
    if field == "is_in_box":
        msg = await callback.message.answer("Відправ нове значення",
                                            reply_markup=choose_goods_type)
    else:
        msg = await callback.message.answer("Відправ нове значення",
                                            reply_markup=ReplyKeyboardRemove())

    await state.update_data(cache_msg=msg)

    await state.set_state(GoodsUpdateState.new_value)
    await callback.answer()


@order_router.message(GoodsUpdateState.new_value)
async def anon(message: Message, state: FSMContext):
    data = await state.get_data()
    new_value = None
    await data['cache_msg'].delete()
    if data['field'] == "photo":
        try:
            new_value = message.photo[-1].file_id
            await message.delete()
        except TypeError:
            await message.reply("❌ Ви повинні відправити фото!",
                                reply_markup=admin_main_kb)
            return

    if not new_value:
        new_value = message.text
    goods = update_goods_field(goods_name=data['goods'].name,
                               field_name=data['field'],
                               new_value=new_value)
    if isinstance(goods, str):
        await message.answer(goods, reply_markup=admin_main_kb)
        return
    goods_model = GoodsModel.from_orm(goods)

    await state.update_data(goods=goods_model)
    msg = build_goods_full_msg(goods_model)
    await message.answer_photo(photo=goods.photo, caption=msg,
                               parse_mode="MARKDOWN",
                               reply_markup=update_goods_inl(goods_model))
