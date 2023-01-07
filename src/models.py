from dataclasses import dataclass


@dataclass
class OrderModel:
    user_id: int
    account_name: str
    city: str
    sex: str
    with_discount: str
    selfie: str
    car: str
    note: str