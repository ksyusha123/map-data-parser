import requests
import json
import hashlib
import sys

from strapi_requests import strapi_login


endpoint = f'https://map-api.ekaterinburg.io/api/{sys.argv[1]}'
token = strapi_login()['jwt']

objects = requests.get(f'{endpoint}?populate=geometry&pagination[page]=1&pagination[pageSize]=10000').json()["data"]
for idx, obj in enumerate(objects):
    geometry = obj['attributes']['geometry']
    if geometry == None:
        continue

    str_coordinates = ','.join(map(str, geometry['coordinates']))
    headers = {"Authorization": f"Bearer {token}"}
    object_id = obj['id']
    response = requests.put(f'{endpoint}/{object_id}', json={
      "data": {
        "CoordinatesHash": hashlib.md5(bytes(str_coordinates, 'utf-8')).hexdigest()
      }
    }, headers=headers)
    if response.status_code != 200:
        print(object_id)