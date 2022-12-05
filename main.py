import json
from typing import List


from osm_requests import get_osm_info_by_free_address, get_osm_info_by_id, get_osm_info_nodes


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


def req(id, type):
    try:
        building_coordinates = get_osm_info_nodes(id, type)
        return building_coordinates
    except:
        print(id)


def add_borders_info_in_file(filepath1):
    with open(filepath1, encoding='utf-8') as f:
        all_okn_objects = json.load(f)
        for obj in all_okn_objects:
            obj['data']['borders'] = req(obj)
    write_json_objects_to_file(all_okn_objects, 'okn/valid_geojson_objects2.json')


def extract_data(filepath1):
    answers = []
    for i in range(1, 19):
        with open(filepath1, encoding='utf-8') as f:
            all_okn_objects = json.load(f)
            for obj in all_okn_objects:
                obj['data']['geometry'] = obj['geometry']
                obj['data']['name'] = obj['data']['name'].replace('"', '\"')
                try:
                    obj['data']['document'] = obj['data']['document'].replace('"', '\"')
                    points = obj['data']['borders']
                    if points is not None and len(points) > 0:
                        obj['data']['borders'] = {'type': 'Polygon', 'coordinates': points}
                except:
                    continue
                answers.append(obj['data'])
    write_json_objects_to_file(answers, 'okn/valid_geojson_objects2.json')


if __name__ == '__main__':
    extract_data()
