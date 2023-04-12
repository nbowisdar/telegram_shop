from src.database.crud.get import reset_goods_cache
from src.database.tables import *
from src.schemas import AddressModel, GoodsModel


def update_addr_field(*, user_id: int, field_name: str, new_value: str):
    addr = User.get(user_id=user_id).address[0]
    setattr(addr, field_name, new_value)
    addr.save()


def update_goods_field(*, goods_name, field_name: str, new_value: str) -> Goods | str:
    try:
        goods = Goods.get(name=goods_name)

        if field_name == "is_in_box":
            if new_value == "📦 В коробках":
                new_value = 1
            else:
                new_value = 0

        setattr(goods, field_name, new_value)
        reset_goods_cache()
        goods.save()
    except Exception as err:
        return str(err)
    return goods


def update_order_status(order_id: int, new_status: str):
    order = Order.get_by_id(order_id)
    order.status = new_status
    order.save()

#
# def decline_order(order_id: int):
#     order = Order.get_by_id(order_id)
#     order.status = "confirmed"
#     order.save()