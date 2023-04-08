from src.schemas import AddressModel, GoodsModel, OrderModel

"""class AddressModel(TypedDict):
    full_name: str
    mobile_number: str
    city: str
    post_number: int
    user: int
"""


def build_address_msg(address: AddressModel) -> str:
    return f"Повне ім'я - *{address.full_name}*\n" \
           f"Мобільний - *{address.mobile_number}*\n" \
           f"Місто - *{address.city}*\n" \
           f"Номер відділення НП - *{address.post_number}*\n"


def build_goods_full_info(g: GoodsModel) -> str:
    return f"*{g.name}* - *{g.price} ₴*\n" \
           f"Опис товару:\n_{g.desc}_"


def build_result_order_msg(order: OrderModel, address: AddressModel, total: float) -> str:
    return f"_Замовлення_:\n" \
           f"Товар - *{order.ordered_goods.name}*\n" \
           f"Кількість - *{order.amount}*\n" \
           f"Ціна - *{order.ordered_goods.price}* ₴\n\n" \
           f"_Адрес доставки_:\n" \
           f"Повне ім'я - *{address.full_name}*\n" \
           f"Мобільний - *{address.mobile_number}*\n" \
           f"Місто - *{address.city}*\n" \
           f"Номер відділення НП - *{address.post_number}*\n\n" \
           f"_Тип оплати_ - *{order.type_payment}*\n_Cумма_ - `{total}` ₴ \n\n" \
