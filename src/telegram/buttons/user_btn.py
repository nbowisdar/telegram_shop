import sys

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from config import categories, buy_variants, buy_variants_box, contact_admin_username
from setup import get_status_pay_card
from src.database.crud.get import get_user_schema_by_id, get_goods_by_category
from src.schemas import GoodsModel

# from src.database.queries import get_all_accounts

kb1 = [
    [KeyboardButton(text="🛒 Обрати товар"), KeyboardButton(text="🕺 Мій профіль")],
    [KeyboardButton(text="💻 Відкрити сайт"), KeyboardButton(text="📞 Контакти")],
    [KeyboardButton(text="✉️ Зв'язок із адміністрацією")]
]

open_site_inl = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💻 Відкрити сайт", url="https://stolichnyy-market.net")]
])

ask_admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✍️ Написати адміністратору", url=f"https://t.me/{contact_admin_username}")]
])

promo_kb = KeyboardButton(text="🧩 Застосувати промокод")

user_main_btn = ReplyKeyboardMarkup(
    keyboard=kb1,
    resize_keyboard=True
)


addr_inline_fields = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Повне ім'я", callback_data="full_name")],
        [InlineKeyboardButton(text="Мобільний номер", callback_data="mobile_number")],
        [InlineKeyboardButton(text="Місто", callback_data="city")],
        [InlineKeyboardButton(text="НП відділення", callback_data="post_number")],
        [InlineKeyboardButton(text="↩️ На головну", callback_data="user_main")]
    ]
)


def build_profile_kb(user_id: int) -> ReplyKeyboardMarkup:
    user = get_user_schema_by_id(user_id)
    if user.address:
        addr_btn = "🔨 Оновити адрес"
    else:
        addr_btn = "🏠 Додати адрес"

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=addr_btn), KeyboardButton(text="📦 Мої замовлення")],
            [KeyboardButton(text="↩️ На головну")]
        ],
        resize_keyboard=True
    )


def get_order_kb(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="☀️ За неділю", callback_data=f"select_order|{user_id}|week"),
             InlineKeyboardButton(text="🗓 За місяць", callback_data=f"select_order|{user_id}|month"),
             InlineKeyboardButton(text="⌚️ За рік", callback_data=f"select_order|{user_id}|year")],
            [InlineKeyboardButton(text="🌎 За весь час", callback_data=f"select_order|{user_id}|all_time")],
        ])


# kb_inline1 = [
#     [InlineKeyboardButton(text="🎩 Запитати на пряму", url="https://t.me/nbowisdar")],
#     [InlineKeyboardButton(text="💻 Відкрити сайт", url="https://stolichnyy-market.net")]
# ]
#
# community_btn = InlineKeyboardMarkup(inline_keyboard=kb_inline1)

ok_goods = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="↩️ З початку", callback_data="order_drop|from_scratch"),
     InlineKeyboardButton(text="Далі ➡️", callback_data="new_order_num|skip")],
    [InlineKeyboardButton(text="❌ Скасувати", callback_data="order_drop|cancel")]
])

cancel_inl_ord = InlineKeyboardButton(text="❌ Скасувати", callback_data="order_drop|cancel")
from_scratch_inl_ord = InlineKeyboardButton(text="↩️ З початку", callback_data="order_drop|from_scratch")
admin_drop_msg = InlineKeyboardButton(text="❌ Закрити", callback_data="admin_drop_msg")





def categories_inl(prefix="new_order_cat", admin=True) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for cat in categories:
        builder.button(
            text=cat, callback_data=f"{prefix}|{cat}"
        )
    builder.adjust(3)
    if not admin:
        builder.row(cancel_inl_ord)
    else:
        builder.row(admin_drop_msg)
    return builder.as_markup()


cancel_shortcut = [InlineKeyboardButton(text="↩️ З початку", callback_data="order_drop|from_scratch"),
                   InlineKeyboardButton(text="❌ Скасувати", callback_data="order_drop|cancel")]


def build_amount_disc_inl(*, price: float, with_desc_btn=True, is_in_box: bool):
    builder = InlineKeyboardBuilder()
    if with_desc_btn:
        builder.row(
            InlineKeyboardButton(text=f"📜 Опис",
                                 callback_data=f"new_order_g|description")
        )
    count = 0
    if is_in_box:
        variants = buy_variants_box
        symbol = "шт"
    else:
        variants = buy_variants
        symbol = "л"

    for amount, percent in variants:
        total = round(
            (price * amount) / 100 * percent)
        builder.row(
            InlineKeyboardButton(text=f"Придбати - {amount} {symbol}. 👉 {total} грн.",
                                 callback_data=f"new_order_addr|{count}")
        )
        count += 1
    # keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    builder.row(
        from_scratch_inl_ord, cancel_inl_ord
    )
    return builder.as_markup()




def build_goods_with_price_inl(category: str, prefix="new_order_g", admin=False,) -> InlineKeyboardMarkup:
    goods: list[GoodsModel] = get_goods_by_category(category.casefold(), admin)
    builder = InlineKeyboardBuilder()

    for g in goods:
        builder.button(
            text=f'{g.name}: Ціна - {g.price} грн/л', callback_data=f"{prefix}|{g.id}"
        )
    builder.adjust(1)
    if not admin:
        builder.row(from_scratch_inl_ord, cancel_inl_ord)
    else:
        builder.row(admin_drop_msg)
    return builder.as_markup()


def build_addr_inl() -> InlineKeyboardMarkup:
    # if get_update_window:
    first_row = [InlineKeyboardButton(text="✅ Так", callback_data="addr_confirmed"),
                 InlineKeyboardButton(text="⚙️ Оновити адресс", callback_data="update_addr")]
    # else:
    #     first_row = [InlineKeyboardButton(text="👌 Продовжити", callback_data="reload_addr")]
    return InlineKeyboardMarkup(inline_keyboard=[
        first_row, cancel_shortcut
    ])


if_promo_inl = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="✅ Так", callback_data="try_discount"),
        InlineKeyboardButton(text="Ні (далі)➡️", callback_data="type_payment")
    ],
    cancel_shortcut
])


def get_delivery_inl() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text="🚛 Наложний платіж", callback_data="payment|later"))

    if get_status_pay_card():
        builder.row(InlineKeyboardButton(text="🚚 Сплатити онлайн", callback_data="payment|now"))
    builder.row(cancel_inl_ord)
    return builder.as_markup()


# type_delivery_inl = InlineKeyboardMarkup(inline_keyboard=[
#     [
#         InlineKeyboardButton(text="🚚 Сплатити онлайн", callback_data="payment|now")
#     ],
#     [InlineKeyboardButton(text="🚛 Наложний платіж", callback_data="payment|later")]
# ])

create_new_ordr_inl = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🛒 Створити замовлення", callback_data="confirm_order")
    ],
    [InlineKeyboardButton(text="❌ Скасувати", callback_data="order_drop|cancel")]
])

show_details = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔍 Перевірити замовлення", callback_data="show_oder_details")]
]
)

pay_inl = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="💳 Я оплатив", callback_data="confirm_pay")
    ],
    [InlineKeyboardButton(text="↩️ З початку", callback_data="order_drop|from_scratch")]
])
