from src.database.crud.get import update_user_addr_cache
from src.database.tables import *
from src.schemas import AddressModel, GoodsModel


def create_address(address: AddressModel):
    user, created = User.get_or_create(user_id=address.user_id)
    user.address = Address.create(**address.dict())

    update_user_addr_cache(address)


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