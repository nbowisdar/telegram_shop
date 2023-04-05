import decimal
from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from setup import user_router
from src.database.crud.get import get_user_schema_by_id, remove_user_from_cache
from src.database.crud.update import update_addr_field
from src.telegram.buttons import addr_inline_fields, admin_main_kb
from src.telegram.messages.user_msg import build_address_msg


class UpdateAddr(StatesGroup):
    field = State()
    new_value = State()

"""
    Not working version
"""


@user_router.message(UpdateAddr.new_value)
async def update_filed(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()

    if data['field'] == "mobile_number":
        try:
            new_value = decimal.Decimal(message.text)
        except decimal.InvalidOperation:
            await state.clear()
            await message.reply("❌ Не вірне значення!")
            return

    elif data['field'] == "photo":
        try:
            new_value = message.photo[-1].file_id
            await message.delete()
        except TypeError:
            await message.reply("❌ Ви повинні відправити фото!",
                                reply_markup=admin_main_kb)
            await state.clear()
            return
    else:
        new_value = message.text

    update_addr_field(
        user_id=message.from_user.id,
        field_name=data['field'],
        new_value=message.text
    )
    remove_user_from_cache(message.from_user.id)

    user = get_user_schema_by_id(message.from_user.id)
    addr = build_address_msg(user.address)
    await message.answer(addr, parse_mode="MARKDOWN", reply_markup=addr_inline_fields)