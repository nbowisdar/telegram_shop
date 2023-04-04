from src.database.tables import *
from src.schemas import AddressModel, GoodsModel, UserModel

users: dict[int, UserModel] = {}


def remove_user_from_cache(user_id):
    if user_id in users.keys():
        del users[user_id]


def get_user_schema_by_id(user_id: int) -> UserModel:
    if user_id in users.keys():
        print("Took from cash!!)")
        return users[user_id]
    user, created = User.get_or_create(user_id=user_id)
    if created:
        return UserModel(user_id=user_id, orders=[], address=None)
    orders = [order for order in user.orders]
    addr = user.address[0].__data__

    user_model = UserModel(user_id=user_id, orders=orders, address=addr)
    users[user_id] = user_model
    return user_model
