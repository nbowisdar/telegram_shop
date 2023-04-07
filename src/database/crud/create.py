from src.database.crud.get import update_user_addr_cache
from src.database.tables import *
from src.schemas import *


def create_address(address: AddressModel):
    user, created = User.get_or_create(user_id=address.user_id)
    user.address = Address.create(**address.dict())
    update_user_addr_cache(address)


def create_goods(goods: GoodsModel) -> bool:
    g, created = Goods.get_or_create(**goods.dict())
    return created


def create_new_order(data: dict) -> Order:
    goods = Goods.get(name=data['goods_name'])
    # promo_code: PromoCodeModel = data['promo_code']
    return Order.create(
        amount=data['amount'],
        discount=data["discount"],
        total=data['total'],
        user=data['user_id'],
        type_payment=data['type_payment'],
        ordered_goods=goods,
    )
    # print('before')
    # return OrderModel.from_orm(order)


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