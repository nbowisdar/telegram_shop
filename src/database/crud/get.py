from pprint import pprint
from typing import Iterable

from src.database.tables import *
from src.schemas import AddressModel, GoodsModel, UserModel, OrderModel, Period
from loguru import logger

cat_name = str
user_id = int

users: dict[user_id, UserModel] = {}
cat_goods: dict[cat_name, list[GoodsModel]] = {}


# def update_user_cache(user: UserModel):
#     users[user.user_id] = user


def update_user_addr_cache(address: AddressModel):
    if address.user_id in users.keys():
        users[address.user_id].address = address
    else:
        users[address.user_id] = UserModel(user_id=address.user_id, address=address, orders=[])


def check_goods_existence(goods_name: str) -> bool:
    for g in Goods.select():
        if g.name == goods_name:
            return True
    return False


def remove_user_from_cache(user_id):
    if user_id in users.keys():
        del users[user_id]


def get_user_schema_by_id(user_id: int) -> UserModel:
    if user_id in users.keys():
        print("Took from cash!!)")
        return users[user_id]
    user, created = User.get_or_create(user_id=user_id)
    if created:
        user_model = UserModel(user_id=user_id, orders=[], address=None)
        users[user_id] = user_model
        return user_model

    orders = [OrderModel.from_orm(order) for order in user.orders]
    if user.address:
        addr = AddressModel.from_orm(user.address.first())
    else:
        addr = None
    user_model = UserModel(user_id=user_id, orders=orders, address=addr)
    users[user_id] = user_model
    return user_model


def get_goods_by_name(name: str) -> GoodsModel:
    return GoodsModel.from_orm(Goods.get(name=name))

"""
class GoodsModel(TypedDict):
    name: str
    desc: str
    category: str
    price: decimal.Decimal
    photo: str
"""


def get_goods_by_category(category: str) -> list[GoodsModel]:
    if category in cat_goods.keys():
        return cat_goods[category]
    goods = Goods.select().where(Goods.category == category)
    resp = [GoodsModel.from_orm(g) for g in goods]
    cat_goods[category] = resp
    return resp


# def get_goods_by_id(id: int) -> Goods:
#     return Goods.get_by


def update_goods_cache(goods: GoodsModel, delete=False):
    goods_list = cat_goods.get(goods.category, [])
    if delete:
        cat_goods[goods.category] = []
        logger.info(f"dropped from cache - {goods.name}")
    else:
        goods_list.append(goods)
        logger.info(f"cached - {goods.name}")


def reset_goods_cache():
    global cat_goods
    cat_goods = {}


def get_users_orders(user_id: int, period: Period) -> list[Order]:
    user = User.get(user_id=user_id)
    return Order.select().where(
        (Order.time_created > period.value) & (Order.user == user)
    )


def get_order_by_id(order_id: int) -> Order | None:
    return Order.get_or_none(id=order_id)


def get_last_orders(user_id, n: int) -> Iterable[Order]:
    user = User.get(user_id=user_id)
    return user.orders.order_by(Order.time_created.desc()).limit(n)


def get_new_users_by_per(period: Period) -> int:
    users = User.select().where(period.value < User.register_time)
    return len(users)


def get_all_users_stat() -> list[tuple[Period: int]]:
    resp = []
    pair = Period.day, get_new_users_by_per(Period.day)
    resp.append(pair)
    pair = Period.week, get_new_users_by_per(Period.week)
    resp.append(pair)
    pair = Period.month, get_new_users_by_per(Period.month)
    resp.append(pair)
    pair = Period.all_time, get_new_users_by_per(Period.all_time)
    resp.append(pair)
    return resp


def find_user_by(finder: str | int) -> None | User:
    if finder.isdigit():
        user = User.get_or_none(user_id=finder)
    else:
        user = User.get_or_none(username=finder)
    return user


def tests():
    x = get_all_users_stat()
    pprint(x)
    # user_id = 286365412
    # #
    # # orders = Order.select().where(Order.user == user)
    # orders = get_users_orders(user_id, Period.all_time)
    # for i in orders:
    #     print(i.ordered_goods)
    # # print(len(orders))


if __name__ == '__main__':
    tests()