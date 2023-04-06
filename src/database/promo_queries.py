from peewee import IntegrityError

from src.database.tables import db, Order, PromoCode, User
import string
import random

from src.schemas import PromoCodeModel


# from src.schemas import AccountModel, OrderModel


def _generate_promo_code(num_char: int) -> str:
    code = ""
    symbl = string.ascii_letters + "0987654321"

    for i in range(num_char):
        code += random.choice(symbl)
    return code[0:4] + "_" + code[4:]


def generate_new_code(*, max_use=10000, discount_percent=10, num_char=8) -> PromoCodeModel:
    code = _generate_promo_code(num_char)
    while True:
        try:
            code = PromoCodeModel(code=code,
                                  max_use=max_use,
                                  discount_percent=discount_percent)
            PromoCode.create(**code.dict())
            print(code.code)
            return code
        except IntegrityError:
            pass


def check_promo(code: str, user_id: int, use=False) -> PromoCodeModel:
    promo = PromoCode.get_or_none(PromoCode.code == code)
    if not promo:
        raise Exception("🛑 Такого промокода не існує!")
    elif promo.max_use <= 0:
        raise Exception("🛑 Цей промокод більше неможно використовувати!")
    user = User.get(user_id=user_id)
    x = [code.code for code in user.codes]
    print(x)
    if code in [code.code for code in user.codes]:
        raise Exception("🛑 Ви вже використовували цей промокод!")
    if use:
        promo.max_use += 1
        promo.save()
    return PromoCodeModel.from_orm(promo)

#
# def get_all_accounts() -> list[AccountModel]:
#     return [
#         AccountModel(name=acc.name, price=acc.price)
#         for acc in Account.select()
#     ]
#
#
# def get_account_by_name(name: str) -> Account:
#     return Account.get(name=name)
#
#
# def create_order(order=OrderModel):
#     Order.create(
#         user_id=order.user_id,
#         account=order.account_id,
#         account_username=order.account_username,
#         city=order.city,
#         sex=order.sex,
#         with_discount=order.with_discount,
#         selfie=order.selfie,
#         car=order.car,
#         note=order.note
#     )
#
#
# def get_order_by_id(order_id: int) -> OrderModel:
#     order = Order.get(id=order_id)
#     return OrderModel(
#         user_id=order.user_id,
#         account_name=order.account.name,
#         account_price=order.account.price,
#         account_username=order.account_username,
#         account_id=None,
#         city=order.city,
#         sex=order.sex,
#         with_discount=order.with_discount,
#         disc_code=None,
#         selfie=order.selfie,
#         car=order.car,
#         note=order.note
#     )
#
#
# def save_code_to_user(user_id: int, code: str):
#     user = UserWithCode.get_or_none(user_id=user_id)
#     if user:
#         raise ValueError("Вы уже использовали промокод!")
#     UserWithCode.create(user_id=user_id, code=code)
#
#
# def is_has_code(user_id: int) -> str | None:
#     user = UserWithCode.get_or_none(user_id=user_id)
#     return user.code
#
#
# def delete_code_from_user(user_id: int):
#     user = UserWithCode.get_or_none(user_id=user_id)
#     if user:
#         user.delete().execute()


# if __name__ == '__main__':
#     save_code_to_user(123, '213')
#     code = is_has_code(123)
#     print(code)
#     delete_code_from_user(123)
