from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from config import categories

cancel_btn = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="❌ Відмінити")]],
    resize_keyboard=True
)


def build_cat_kb(is_admin=False) -> InlineKeyboardMarkup:
    if is_admin:
        prefix = "add_goods"
    else:
        prefix = "choose"
    builder = InlineKeyboardBuilder()
    for cat in categories:
        builder.button(
            text=cat, callback_data=f"{prefix}|{cat}"
        )
    builder.adjust(4)
    return builder.as_markup()