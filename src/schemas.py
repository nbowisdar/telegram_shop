# from dataclasses import dataclass
import decimal
from typing import NamedTuple, TypedDict

from src.database.tables import Order


class AddressModel(TypedDict):
    full_name: str
    mobile_number: str
    city: str
    post_number: int
    user: int


class GoodsModel(TypedDict):
    name: str
    desc: str
    price: decimal.Decimal
    photo: str


class UserModel(NamedTuple):
    user_id: int
    orders: list[Order]
    address: AddressModel | None
