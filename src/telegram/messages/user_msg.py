from src.schemas import AddressModel

"""class AddressModel(TypedDict):
    full_name: str
    mobile_number: str
    city: str
    post_number: int
    user: int
"""


def build_address_msg(address: AddressModel) -> str:
    return f"Повне ім'я - *{address['full_name']}*\n" \
           f"Мобільний - *{address['mobile_number']}*\n" \
           f"Місто - *{address['city']}*\n" \
           f"Номер відділення НП - *{address['post_number']}*\n"
