import json

from main import write_json_objects_to_file, req


def add_info_in_file(filepath1, filepath2):
    with open(filepath1, encoding='utf-8') as f:
        all_okn_objects = json.load(f)
        for obj in all_okn_objects:
            number = obj['data']['okn_number']
            with open(filepath2, encoding='utf-8') as f2:
                data_obj = json.load(f2)
                for d in data_obj:
                    if d["Номер в реестре"] == number:
                        obj['data']['document'] = d["наименование документа"].replace('"', '\'')
    write_json_objects_to_file(all_okn_objects,
                               'okn/valid_geojson_objects.json')


