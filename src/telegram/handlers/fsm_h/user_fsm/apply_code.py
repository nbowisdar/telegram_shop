from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.database.queries import check_promo


class UseCode(StatesGroup):
    user_id = State()
    code = State()


async def use_code(message: Message, state: FSMContext):
    pass
