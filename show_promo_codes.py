from src.database.tables import PromoCode
from dataclasses import dataclass

@dataclass
class CodeModel:
    name: str
    used: int


def main():
    codes = [CodeModel(
        name=code.name, used=code.count_of_use)
        for code in PromoCode.select()]

    for code in sorted(codes, key=lambda x: x.used):
        print(f'{code.name} - used - {code.used} times')


if __name__ == '__main__':
    main()

