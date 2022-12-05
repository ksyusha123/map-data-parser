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
                feature_osm = get_osm_info_by_id(id, type)
                borders = {'type': 'Polygon', 'coordinates': req(id, 'way')}
                feature = {'building': obj['properties']['BUILDING'], 'floors': obj['properties']['B_LEVELS'],
                           'address': f'{obj["properties"]["A_STRT"]}, {obj["properties"]["A_HSNMBR"]}',
                           'name': obj['properties']['NAME'], 'borders': borders}
                if 'error' not in feature_osm:
                    feature['geometry'] = feature_osm['geometry']
                all_f.append(feature)
            except:
                all_f_error.append(obj)


        write_json_objects_to_file(all_f_error,
                                   'data_center_constructions/valid_geojson_objects_out_center5.json')
        write_json_objects_to_file(all_f, 'data_center_constructions/valid_geojson_objects_out_center.json')
