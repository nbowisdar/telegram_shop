from config import buy_variants_box, buy_variants
from src.schemas import AddressModel, GoodsModel, OrderModel

"""class AddressModel(TypedDict):
    full_name: str
    mobile_number: str
    city: str
    post_number: int
    user: int
"""


def build_msg_discount_amount(goods: GoodsModel, is_in_box: bool, with_desc=False) -> str:
    if is_in_box:
        variants = buy_variants_box
        symbol = "шт"
        full_smb = "коробок"
        sml = "📦"
    else:
        variants = buy_variants
        symbol = "л"
        full_smb = "літрів"
        sml = "🔵"
    res = [f"*{goods.name}*\n"]
    for amount, discount in variants:
        price_with_discount = round(
            (goods.price) / 100 * discount, 2)
        res.append(
            f"{sml} {amount} {full_smb} — {price_with_discount} грн / {symbol}."
        )
    if with_desc:
        res.append(f"\n{goods.desc}")
    return "\n".join(res)


def build_address_msg(address: AddressModel) -> str:
    return f"Повне ім'я - *{address.full_name}*\n" \
           f"Мобільний - *{address.mobile_number}*\n" \
           f"Місто - *{address.city}*\n" \
           f"Номер відділення НП - *{address.post_number}*\n"


def build_goods_full_info(g: GoodsModel) -> str:
    return f"{g.name}* - *{g.price} грн/л\n" \
           f"Опис товару:\n_{g.desc}_"


def build_result_order_msg(order: OrderModel, address: AddressModel, total: float) -> str:
    return f"_Замовлення_:\n" \
           f"Товар - *{order.ordered_goods.name}*\n" \
           f"Кількість - *{order.amount_disc.amount}*\n" \
           f"Ціна - *{order.ordered_goods.price}* грн/л\n\n" \
           f"_Адрес доставки_:\n" \
           f"Повне ім'я - *{address.full_name}*\n" \
           f"Мобільний - *{address.mobile_number}*\n" \
           f"Місто - *{address.city}*\n" \
           f"Номер відділення НП - *{address.post_number}*\n\n" \
           f"_Тип оплати_ - *{order.type_payment}*\n" \
           f"_Cумма (З урахуванням знижки)_ - `{total}` ₴ \n\n"
