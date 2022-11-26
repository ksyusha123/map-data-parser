import json

from main import write_json_objects_to_file


def change_pos_geo(file_name):
    with open(file_name, encoding='utf-8') as f:
        all_objects = json.load(f)
        all_f = []
        for obj in all_objects:
            for coord in obj['geometry']['coordinates'][0][0]:
                coord[0], coord[1] = coord[1], coord[0]
            all_f.append(obj)
    write_json_objects_to_file(all_f, 'okn/valid_security_zone.json')