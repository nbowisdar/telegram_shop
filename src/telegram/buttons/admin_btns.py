from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from setup import get_status
from src.schemas import GoodsModel
from src.telegram.middleware.check_bot_online import blocked_users

admin_drop_msg = InlineKeyboardButton(text="❌ Закрити", callback_data="admin_drop_msg")

admin_cancel_btn = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🛑 Відмінити")]],
    resize_keyboard=True
)

admin_main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛍 Товари"),
         KeyboardButton(text="📊 Замовлення"),
         KeyboardButton(text="💾 Інше")],
        [KeyboardButton(text="📈 Статистика"),
         KeyboardButton(text="🔑 Створити новий промокод")]
    ],
    resize_keyboard=True
)

on_main_admin_kb = KeyboardButton(text="⬅️ На головну")

admin_goods_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✏️ Додати"), KeyboardButton(text="🔨 Оновити")],
        [KeyboardButton(text="⬅️ На головну")]
    ],
    resize_keyboard=True
)

choose_goods_type = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="📦 В коробках"), KeyboardButton(text="🍾 В літрах")],
    [KeyboardButton(text="🛑 Відмінити")]
],  resize_keyboard=True)


"Inline keyboards bellow"


def delete_or_update_one(id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="♻️ Оновити", callback_data=f"change_one|update|{id}"),
            InlineKeyboardButton(text="🗑 Видалити", callback_data=f"change_one|delete|{id}")
        ],
        [admin_drop_msg]
    ])


confirm_order_inl = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="✅ Підтвердити", callback_data="order_waiting|confirm"),
        InlineKeyboardButton(text="🛑 Відхилити", callback_data="order_waiting|decline")
    ],
])


def update_goods_inl(goods: GoodsModel) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"✍️ Назва", callback_data="update_goods_field|name")],
        [InlineKeyboardButton(text=f"📝 Опис", callback_data="update_goods_field|desc")],
        [InlineKeyboardButton(text=f"💵 Ціна", callback_data="update_goods_field|price")],
        [InlineKeyboardButton(text=f"🖌 Тип", callback_data="update_goods_field|is_in_box")],
        [InlineKeyboardButton(text=f"📷 Фото", callback_data="update_goods_field|photo")],
        [admin_drop_msg]
    ])


def other_bot_btn() -> ReplyKeyboardMarkup:
    # print(get_status())
    if get_status():
        action = "🛑 Зупинити бота"
    else:
        action = "🚀 Запустити бота"

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=action)], [KeyboardButton(text="📫 Розіслати повідомлення")],
            [KeyboardButton(text="⬅️ На головну")]
        ],
        resize_keyboard=True
    )


find_order_option = ReplyKeyboardMarkup(keyboard=[
    [InlineKeyboardButton(text=f"🔍 Знайти замовлення"),
     InlineKeyboardButton(text=f"🔍 Знайти користувача")],
    [on_main_admin_kb]
], resize_keyboard=True)


def action_with_found_user(user_id) -> InlineKeyboardMarkup:
    if int(user_id) in blocked_users:
        text, action = "🤝 Розблокувати", "unblock"
    else:
        text, action = "👮‍♀️ Заблокувати", "block"

    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Останні 10 замовлень", callback_data=f"found_user|last_10_order|{user_id}"),
            InlineKeyboardButton(text=text, callback_data=f"found_user|{action}|{user_id}"),
        ],
        [InlineKeyboardButton(text="❌ Закрити", callback_data="to_main_admin_drop_msg")]
    ])


def update_status_order_inl(order_id) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="♻️ Оновити статус", callback_data=f"update_order_status|{order_id}"),
        ],
        [InlineKeyboardButton(text="❌ Закрити", callback_data="to_main_admin_drop_msg")]
    ])


def update_status_order_choice(order_id) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Підтвердженно", callback_data=f"update_order_choice|{order_id}|confirmed"),
            InlineKeyboardButton(text="🛑 Скасованно", callback_data=f"update_order_choice|{order_id}|canceled"),
            InlineKeyboardButton(text="🎉 Виконанно", callback_data=f"update_order_choice|{order_id}|executed"),
        ], [InlineKeyboardButton(text="❌ Закрити", callback_data="to_main_admin_drop_msg")]
    ])


new_users_select_per_inl = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🔰 За добу", callback_data="new_user_stat|day"),
        InlineKeyboardButton(text="⌚️ За неділю", callback_data="new_user_stat|week"),
        InlineKeyboardButton(text="🗓 За місяць", callback_data="new_user_stat|month"),
    ], [InlineKeyboardButton(text="🌎 Юзерів загалом", callback_data="new_user_stat|all_time"),
        InlineKeyboardButton(text="📊 Уся статистика", callback_data="new_user_stat|all_new_user_stat")],
    [admin_drop_msg]
])
