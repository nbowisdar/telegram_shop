from src.database.tables import *
from src.schemas import AddressModel, GoodsModel


def update_addr_field(*, user_id: int, field_name: str, new_value: str):
    addr = User.get(user_id=user_id).address[0]
    setattr(addr, field_name, new_value)
    addr.save()
