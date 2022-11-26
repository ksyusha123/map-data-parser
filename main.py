import json
from typing import List

from okn.add_info_in_file import add_info_in_file


def write_json_objects_to_file(json_objects: List, filename: str):
    with open(filename, 'w', encoding='utf-8') as file:
        string_object = json.dumps(json_objects, indent=4)
        string_object = string_object.encode('latin-1').decode(
            'unicode_escape')
        file.write(string_object)


def delete_request():
    m = []
    k = []
    for i in range(1, 1000):
        k.append(i)
    for i in range(1000, 2000):
        m.append(i)
    print(m)
    print(k)


if __name__ == '__main__':
    add_info_in_file('okn/valid_geojson_objects.json', 'okn/data_okn.json')
