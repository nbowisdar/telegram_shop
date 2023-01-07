from dataclasses import dataclass
from typing import NamedTuple


@dataclass
class OrderModel:
    user_id: int
    # order_id: int
    account_name: str
    account_price: float
    account_id: int | None
    city: str
    sex: str
    with_discount: bool
    disc_code: str | None
    selfie: str
    car: str | None
    note: str | None


@dataclass
class AccountModel:
    name: str
    price: float
