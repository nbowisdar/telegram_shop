from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.database.queries import get_all_accounts

kb1 = [
    [KeyboardButton(text="Цена Аккаунтов💸"), KeyboardButton(text="Купить аккаунт⚡️")],
    [KeyboardButton(text="Тех поддержка💻"), KeyboardButton(text="Наш канал🎩")],
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


def build_acc_btns() -> ReplyKeyboardMarkup:
    accounts = get_all_accounts()
    builder = ReplyKeyboardBuilder()
    for acc in accounts:
        builder.add(KeyboardButton(text=acc.name))
    builder.adjust(4)
    return builder.as_markup(resize_keyboard=True)