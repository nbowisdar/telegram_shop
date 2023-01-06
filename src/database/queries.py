from src.database.tables import db, Service, Order, PromoCode


def _get_promo():
    pass


def check_promo(name: str) -> bool:
    promo = PromoCode.get_or_none(PromoCode.name == name)
    if not promo:
        return False
    promo.count_of_use += 1
    promo.save()
    return True


if __name__ == '__main__':
    #PromoCode.create(name="test")
    x = check_promo("test")
    print(x)