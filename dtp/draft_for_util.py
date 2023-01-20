from __future__ import annotations

import json

import requests
from datetime import datetime

from strapi_requests import post_new_dtp_object, strapi_login


def download_file():
    response = requests.get('http://cms.dtp-stat.ru/media/opendata/sverdlovskaia-oblast.geojson')
    return response.json()


def parse_dtp(mm=None, yyyy=None, filename=None):
    token = strapi_login()['jwt']
    object_to_file = []
    if mm is None:
        mm = datetime.now().month - 1
    if yyyy is None:
        if mm == 12:
            yyyy = datetime.now().year - 1
        else:
            yyyy = datetime.now().year
    if filename is not None:
        with open(filename, encoding='utf-8') as file:
            all_dtps = json.load(file)
            filter_data(all_dtps, yyyy, mm, object_to_file)
    else:
        res = download_file()['features']
        filter_data(res, yyyy, mm, object_to_file)

    for obj in object_to_file:
        res = post_new_dtp_object(token, obj)


def filter_data(all_dtps, yyyy, mm, object_to_file):
    for dtp in all_dtps:
        if dtp["properties"]["region"] is not None:
            if "Екатеринбург" in dtp["properties"]["region"] and f'{yyyy}-{mm}' in dtp["properties"]["datetime"]:
                dtp_obj = {}
                dtp_obj = dtp['properties']
                dtp_obj['geometry'] = dtp['geometry']
                object_to_file.append(dtp_obj)
