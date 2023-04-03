from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.database.crud.get import get_user_schema_by_id

# from src.database.queries import get_all_accounts

kb1 = [
    [KeyboardButton(text="🛒 Обрати товар"), KeyboardButton(text="🕺 Мій профіль")],
    [KeyboardButton(text="✍️ Зворотній зв'язок"), KeyboardButton(text="🧩 Застосувати промокод")]
]

user_main_btn = ReplyKeyboardMarkup(
    keyboard=kb1,
    resize_keyboard=True
)


def build_profile_kb(user_id: int) -> ReplyKeyboardMarkup:
    user = get_user_schema_by_id(user_id)
    if user.address:
        addr_btn = "🔨 Оновити адрес"
    else:
        addr_btn = "🏠 Додати адрес"

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=addr_btn), KeyboardButton(text="📦 Мої замовлення")]
        ],
        resize_keyboard=True
    )


kb_inline1 = [
    [InlineKeyboardButton(text="🎩 Запитати на пряму", url="https://t.me/nbowisdar")],
    [InlineKeyboardButton(text="💻 Наш сайт", url="https://stolichnyy-market.net")]
]

community_btn = InlineKeyboardMarkup(inline_keyboard=kb_inline1)


def build_acc_btns() -> ReplyKeyboardMarkup:
    # accounts = get_all_accounts()
    accounts = []
    builder = ReplyKeyboardBuilder()
    for acc in accounts:
        builder.add(KeyboardButton(text=acc.name))
    builder.adjust(4)
    return builder.as_markup(resize_keyboard=True)