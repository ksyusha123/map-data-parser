import json

from main import write_json_objects_to_file
from osm_requests import get_osm_info_by_id


def process(file_name):
    with open(file_name, encoding='utf-8') as f:
        all_objects = json.load(f)
        all_f = []
        all_f_error = []
        for obj in all_objects:
            try:
                id = obj['properties']['OSM_ID']
                type = obj['properties']['OSM_TYPE'][0].upper()
                print(id)
                feature = get_osm_info_by_id(id, type)
                feature['data'] = {}
                feature['data']['building'] = obj['properties']['BUILDING']
                feature['data']['floors'] = obj['properties']['B_LEVELS']
                feature['data']['street'] = obj['properties']['A_STRT']
                feature['data']['house_number'] = obj['properties']['A_HSNMBR']
                feature['data']['name'] = obj['properties']['NAME']
                all_f.append(feature)
            except:
                all_f_error.append(obj)


        write_json_objects_to_file(all_f_error, 'invalid_geojson_objects_out_center.json')
        write_json_objects_to_file(all_f, 'data_center_constructions/valid_geojson_objects_out_center.json')