from aiogram.types import Message

from src.database.tables import Order, order_status
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


def build_users_orders_msg(orders: list[Order]) -> str:
    order_list = []
    for order in orders:
        readable_status = order_status.get(order.status)
        order_msg = f"_Замовлення_ - `{order.id}`\n" \
                    f"Число - *{order.time_created.date()}*\n" \
                    f"Товар - *{order.ordered_goods.name}*\n" \
                    f"Кількість - *{order.amount}*\n" \
                    f"Сумма - *{order.amount}* ₴\n" \
                    f"Статус - *{readable_status}*"
        order_list.append(order_msg)

    return "\n\n".join(order_list)
