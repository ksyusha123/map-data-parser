from __future__ import annotations

import json

import requests

from strapi_requests import post_new_dtp_object, strapi_login


def download_file():
    response = requests.get('https://cms.dtp-stat.ru/media/opendata/sverdlovskaia-oblast.geojson')
    return response.json()


def parse_dtp(mm: str, filename=None):
    token = strapi_login()['jwt']
    object_to_file = []
    if filename is not None:
        with open(filename, encoding='utf-8') as file:
            all_dtps = json.load(file)
            filter_data(all_dtps, mm, object_to_file)
    else:
        res = download_file()['features']
        filter_data(res, mm, object_to_file)

    for obj in object_to_file:
        res = post_new_dtp_object(token, obj)


def filter_data(all_dtps, mm, object_to_file):
    for dtp in all_dtps:
        if dtp["properties"]["region"] is not None:
            if "Екатеринбург" in dtp["properties"]["region"] and f'2022-{mm}' in dtp["properties"]["datetime"]:
                object_to_file.append(dtp)
