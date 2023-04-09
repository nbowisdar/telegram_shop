from typing import Iterable

from aiogram.types import Message

from src.database.tables import Order, order_status, type_payment
from src.schemas import AddressModel, GoodsModel, OrderModel

'''
class GoodsModel(Base):
    name: str
    desc: str
    category: str
    price: decimal.Decimal
    photo: str
'''


def build_goods_full_msg(goods: GoodsModel):
    return f"Назва - _{goods.name}_\n" \
           f"Опис - _{goods.desc}_\n" \
           f"Категорія - _{goods.category}_\n" \
           f"Ціна - *{float(goods.price)}* ₴\n"


def build_users_orders_msg(orders: Iterable[Order]) -> str:
    order_list = []
    for order in orders:
        readable_status = order_status.get(order.status)
        order_msg = f"_Замовлення_ - `{order.id}`\n" \
                    f"Число - *{order.time_created.date()}*\n" \
                    f"Товар - *{order.ordered_goods.name}*\n" \
                    f"Кількість - *{order.amount}*\n" \
                    f"Сумма - *{order.total}* ₴\n" \
                    f"Статус - *{readable_status}*"
        order_list.append(order_msg)

    return "\n\n".join(order_list)


def build_order_info_for_admin(order: Order) -> str:
    readable_status = order_status.get(order.status)
    address = order.user.address.first()
    p_type = type_payment[order.type_payment]

    return f"_Замовлення_ - `{order.id}`\n" \
           f"Число - *{order.time_created.date()}*\n" \
           f"Товар - *{order.ordered_goods.name}*\n" \
           f"Кількість - *{order.amount}*\n" \
           f"_Адрес доставки_:\n" \
           f"Повне ім'я - *{address.full_name}*\n" \
           f"Мобільний - *{address.mobile_number}*\n" \
           f"Місто - *{address.city}*\n" \
           f"Номер відділення НП - *{address.post_number}*\n\n" \
           f"_Тип оплати_ - *{p_type}*\n" \
           f"_Cумма_ - `{order.total}` ₴\n" \
           f"Статус - *{readable_status}*"

