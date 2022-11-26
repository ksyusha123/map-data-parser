import requests


def get_osm_info_by_parsed_address(city: str, street: str, house_number: str) -> dict:
    address = f"{house_number} {street}"
    response = requests.get(f'https://nominatim.openstreetmap.org/'
                            'search?'
                            f'street={address}&city={city}'
                            '&format=geojson')
    return response.json()


def get_osm_info_by_free_address(address: str) -> dict:
    response = requests.get(f'https://nominatim.openstreetmap.org/'
                            'search?'
                            f'q={address}'
                            '&format=geojson')
    return response.json()


def get_osm_info_by_id(id: str, type: str) -> dict:
    response = requests.get(f'https://nominatim.openstreetmap.org/details?'
                            f'osmid={id}'
                            f'&osmtype={type}'
                            '&format=json')
    return response.json()
