# from dataclasses import dataclass
import decimal
from typing import NamedTuple, TypedDict


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
