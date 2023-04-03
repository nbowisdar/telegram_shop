from src.database.tables import *
from src.schemas import AddressModel, GoodsModel


def create_address(address: AddressModel, user_id: int):
    user, created = User.get_or_create(user_id=user_id)
    address['user'] = user
    user.address = Address.create(**address)


def create_goods(goods: GoodsModel):
    Goods.create(**goods)


def tests():
    """
    full_name: str
    mobile_number: str
    city: str
    post_number: int
    """

    address = AddressModel(full_name="Vova Fed", mobile_number="098123", city="Dnipro", post_number=123)
    create_address(address, 1)

if __name__ == '__main__':
    tests()