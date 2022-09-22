import json
import re
import requests
from typing import Tuple, List

categories = []


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


def process_house_number(raw_house_number: str) -> str:
    return raw_house_number.replace('д. ', '')


def process_street(raw_street: str) -> str:
    return raw_street.replace('ул. ', '')


def process_city(raw_city: str) -> str:
    return raw_city.replace('г. ', '')


def parse_address(address: str) -> Tuple[str, str, str] | None:
    parts = address.split(', ')
    if len(parts) != 4:
        return None

    region, raw_city, raw_street, raw_house_number = \
        parts[0], parts[1], parts[2], parts[3]

    city = process_city(raw_city)
    street = process_street(raw_street)
    house_number = process_house_number(raw_house_number)

    return city, street, house_number


def write_json_objects_to_file(json_objects: List, filename: str):
    with open(filename, 'w', encoding='utf-8') as file:
        string_object = json.dumps(json_objects, indent=4)
        string_object = string_object.encode('latin-1').decode(
            'unicode_escape')
        file.write(string_object)


def process_name(old_name: str) -> str:
    return old_name.replace('ё', 'е').replace('-', '').lower()


def has_house_street_structure(name: str, street: str, house_number: str) -> bool:
    return re.search(rf"{house_number}, [улица |проспект |набережная ]*"
                     rf"{street}", name) is not None


def process_okn_object(obj, okn_objects_with_unusual_address,
                       valid_geojson_objects,
                       objects_without_concrete_building,
                       too_many_features_and_nothing_found):
    raw_address = obj["Полный адрес"]
    parsed_address = parse_address(raw_address)
    if not parsed_address:
        okn_objects_with_unusual_address.append(obj)
        return
    city, street, house_number = parsed_address

    osm_info = get_osm_info_by_parsed_address(city, street, house_number)
    features = []
    house_number = house_number.lower()
    street = street.lower()

    object_features = osm_info['features']
    if len(object_features) == 1:
        valid_geojson_objects.append(object_features[0])
        return

    for feature in object_features:
        name = process_name(feature['properties']['display_name'])
        if has_house_street_structure(name, street, house_number):
            features.append(feature)

    if len(features) == 0:
        print('не смог найти конкретное здание')
        print(parsed_address)
        print(osm_info, end='\n\n')
        objects_without_concrete_building.append(obj)

    elif len(features) == 1:
        valid_geojson_objects.append(features[0])

    else:
        found_needed_category = False
        for feature in features:
            category = feature['properties']['category']
            categories.append(category)

            if category == 'historic':
                valid_geojson_objects.append(feature)
                found_needed_category = True
                break
            if category == 'building':
                valid_geojson_objects.append(feature)
                found_needed_category = True
                break

        if not found_needed_category:
            print("not found")
            print(parsed_address)
            print(osm_info, end='\n\n')
            too_many_features_and_nothing_found.append(osm_info)


def print_stats(valid_geojson_objects,
                okn_objects_with_unusual_address,
                objects_without_concrete_building,
                too_many_features_and_nothing_found
                ):
    print(f"Valid geojson objects: {len(valid_geojson_objects)}")
    print(f"Okn objects with unusual address:"
          f" {len(okn_objects_with_unusual_address)}")
    print(f"objects_without_concrete_building: {len(objects_without_concrete_building)}")
    print(f"too_many_features_and_nothing_found: {len(too_many_features_and_nothing_found)}")


def main(filepath: str):
    valid_geojson_objects = []
    okn_objects_with_unusual_address = []
    objects_without_concrete_building = []
    too_many_features_and_nothing_found = []

    with open(filepath, encoding='utf-8') as f:
        all_okn_objects = json.load(f)
        for obj in all_okn_objects:
            process_okn_object(obj, okn_objects_with_unusual_address,
                               valid_geojson_objects,
                               objects_without_concrete_building,
                               too_many_features_and_nothing_found)

    write_json_objects_to_file(valid_geojson_objects,
                               '../valid_geojson_objects.json')
    write_json_objects_to_file(okn_objects_with_unusual_address,
                               '../okn_objects_with_unusual_address.json')
    write_json_objects_to_file(objects_without_concrete_building,
                               '../objects_without_concrete_building.json')
    write_json_objects_to_file(too_many_features_and_nothing_found,
                               '../too_many_features_and_nothing_found.json')

    print_stats(valid_geojson_objects, okn_objects_with_unusual_address,
                objects_without_concrete_building, too_many_features_and_nothing_found)


if __name__ == '__main__':
    main('data_okn.json')
