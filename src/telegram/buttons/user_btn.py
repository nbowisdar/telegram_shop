from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# from src.database.queries import get_all_accounts

kb1 = [
    [KeyboardButton(text="Цена Аккаунтов💸"), KeyboardButton(text="Додати адрес🏠")],
    [KeyboardButton(text="Обратная связь✍️"), KeyboardButton(text="Применить промокод🧩")]
]

user_main_btn = ReplyKeyboardMarkup(
    keyboard=kb1,
    resize_keyboard=True
)


kb2 = [
    [KeyboardButton(text="Мужчина"), KeyboardButton(text="Женщина")],
]

sex_btn = ReplyKeyboardMarkup(
    keyboard=kb2,
    resize_keyboard=True
)


kb_inline1 = [
    [InlineKeyboardButton(text="Тех поддержка💻", url="https://t.me/smblikeme")],
    [InlineKeyboardButton(text="Наш канал🎩", url="https://t.me/test_channel_chicago")]
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