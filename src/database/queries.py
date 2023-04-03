from src.database.tables import db, Order, PromoCode
import string
import random

# from src.schemas import AccountModel, OrderModel


def _generate_promo_code(num_char: int) -> str:
    code = ""
    symbl = string.ascii_letters + "0987654321"

    for i in range(num_char):
        code += random.choice(symbl)
    return code[0:4] + "_" + code[4:]


def generate_new_code(num_char=8) -> str:
    code = _generate_promo_code(num_char)
    PromoCode.create(code=code)
    print(code)
    return code


def check_promo(code: str, incr_amount=False) -> str | None:
    promo = PromoCode.get_or_none(PromoCode.code == code)
    if not promo:
        return
    if incr_amount:
        promo.count_of_use += 1
        promo.save()
    return code

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
