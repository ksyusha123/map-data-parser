import re

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
                            f'q={address}, Екатеринбург'
                            '&format=geojson')
    return response.json()


def get_osm_info_by_id(id: str, type: str) -> dict:
    response = requests.get(f'https://nominatim.openstreetmap.org/details?'
                            f'osmid={id}'
                            f'&osmtype={type}'
                            '&format=json')
    return response.json()


def get_osm_info_nodes(id: str, type: str) -> dict:
    ans = []
    pattern = r'<nd ref="(\d+?)"/>'
    response = requests.get(f'https://www.openstreetmap.org/api/0.6/{type}/{id}?xhr=1')
    match = re.findall(pattern, response.text)
    if match is not None:
        for i in match:
            new_response = requests.get(f'https://www.openstreetmap.org/api/0.6/node/{i}?xhr=1')
            other_pattern = r'lat="([\d\.]+?)" lon="([\d\.]+?)"'
            coord = re.findall(other_pattern, new_response.text)
            ans.append([float(coord[0][0]), float(coord[0][1])])
    return ans
