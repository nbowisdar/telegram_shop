from src.database.tables import *
from src.schemas import AddressModel, GoodsModel


def update_addr_field(*, user_id: int, field_name: str, new_value: str):
    addr = User.get(user_id=user_id).address[0]
    setattr(addr, field_name, new_value)
    addr.save()


def update_order_status(order_id: int, new_status: str):
    order = Order.get_by_id(order_id)
    order.status = new_status
    order.save()

#
# def decline_order(order_id: int):
#     order = Order.get_by_id(order_id)
#     order.status = "confirmed"
#     order.save()