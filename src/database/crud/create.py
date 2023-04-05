from src.database.tables import *
from src.schemas import AddressModel, GoodsModel


def create_address(address: AddressModel, user_id: int):
    user, created = User.get_or_create(user_id=user_id)
    address['user'] = user
    user.address = Address.create(**address.dict())


def create_goods(goods: GoodsModel) -> bool:
    g, created = Goods.get_or_create(**goods.dict())
    return created

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