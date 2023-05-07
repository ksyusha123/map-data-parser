import requests

from osm_requests import get_osm_info_by_free_address, get_osm_info_nodes
from strapi_requests import strapi_login

endpoint = f'https://map-api.ekaterinburg.io/api/house'
token = strapi_login()['jwt']

objects = requests.get(f'{endpoint}?populate=borders&pagination[page]=1&pagination[pageSize]=10000').json()["data"]
headers = {"Authorization": f"Bearer {token}"}
for idx, obj in enumerate(objects):
    if 'borders' in obj['attributes']:
        if 'пр-кт' in obj['attributes']['Address'] and obj['attributes']['borders'] is None:
            object_id = obj['id']
            address = obj['attributes']['Address'].replace('пр-кт', '')
            address = address.replace('г. Екатеринбург,', '')
            address = address.replace('Екатеринбург,', '')
            address = address.replace('ул. ', '')
            address = address.replace(',', '')
            address = address.replace('Свердловская область', '').strip()
            features = get_osm_info_by_free_address(address)['features']
            for feature in features:
                if feature['properties']['osm_type'] == 'way':
                    info = get_osm_info_nodes(feature['properties']['osm_id'], 'way')
                    response = requests.put(f'{endpoint}/{object_id}', json={
                      "data": {
                        "borders": {'coordinates': info, 'type':'Polygon'}
                      }
                    }, headers=headers)
                    break
