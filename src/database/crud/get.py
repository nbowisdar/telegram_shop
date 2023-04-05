from src.database.tables import *
from src.schemas import AddressModel, GoodsModel, UserModel, OrderModel

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
        print(users[user_id])
        print("Took from cash!!)")
        return users[user_id]
    user, created = User.get_or_create(user_id=user_id)
    if created:
        return UserModel(user_id=user_id, orders=[], address=None)
    orders = [OrderModel.from_orm(order) for order in user.orders]
    if user.address:
        # addr = AddressModel(**user.address[0].__data__)
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
    resp = [GoodsModel(**g.__data__) for g in goods]
    cat_goods[category] = resp
    return resp
