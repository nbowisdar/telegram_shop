from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from setup import user_router
from src.database.crud.get import get_user_schema_by_msg, remove_user_from_cache
from src.database.crud.update import update_addr_field
from src.telegram.buttons import addr_inline_fields
from src.telegram.messages.user_msg import build_address_msg


class UpdateAddr(StatesGroup):
    field = State()
    new_value = State()


@user_router.message(UpdateAddr.new_value)
async def update_filed(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()

    if data['field'] == "mobile_number":
        number = message.text
        if not number.isdigit() or len(number) != 12 or not number.startswith("380"):
            await state.clear()
            await message.reply("Не вірний формат!\nНомер має починатися з 380")
            return
    elif data['field'] == "post_number":
        if not message.text.isdigit():
            await state.clear()
            await message.reply("Не вірний формат!")
            return

    user_id = message.from_user.id
    update_addr_field(
        user_id=user_id,
        field_name=data['field'],
        new_value=message.text
    )
    remove_user_from_cache(user_id)

    user = get_user_schema_by_msg(message)
    addr = build_address_msg(user.address)
    await message.answer(addr, parse_mode="MARKDOWN", reply_markup=addr_inline_fields)