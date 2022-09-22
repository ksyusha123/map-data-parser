from typing import Tuple
import re


def process_house_number(raw_house_number: str) -> str:
    return raw_house_number.replace('д. ', '')


def process_street(raw_street: str) -> str:
    return raw_street.replace('ул. ', '').replace('пр. ', '')


def process_city(raw_city: str) -> str:
    return raw_city.replace('г. ', '').replace('город ', '')


def parse_address(address: str) -> Tuple[str, str, str] | None:
    address = address.lower()

    address = re.sub(r'\/.*', '', address)

    tokens = address.split(', ')

    if len(tokens) >= 3 and 'район' in tokens[2]:
        tokens.pop(2)

    if len(tokens) >= 5:
        # еще есть кейс с литером
        if 'корп.' in tokens[4]:
            num = tokens[4].split(' ')[1].split(', ')[0]
            tokens[3] += f'/{num}'
        tokens = tokens[:4]

    if len(tokens) != 4:
        return None

    region, raw_city, raw_street, raw_house_number = \
        tokens[0], tokens[1], tokens[2], tokens[3]

    city = process_city(raw_city)
    street = process_street(raw_street)
    house_number = process_house_number(raw_house_number)

    return city, street, house_number


def parse_free_address(raw_address: str) -> str:
    return ' '.join(raw_address.split(', ')[1:]).replace('г. ', '')


def process_name(old_name: str) -> str:
    return old_name.replace('ё', 'е').replace('-', '').lower()


def has_house_street_structure(name: str, street: str, house_number: str) -> bool:
    return re.search(rf"{house_number}, [улица |проспект |набережная ]*"
                     rf"{street}", name) is not None
