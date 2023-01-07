from dataclasses import dataclass


@dataclass
class OrderModel:
    user_id: int
    account_name: str
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
