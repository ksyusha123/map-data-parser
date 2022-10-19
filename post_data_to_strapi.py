import json
import requests

strapi_url = 'http://localhost:1337/api/okns'

jwt = ''


def post_to_strapi(full_okn: dict) -> requests.Response:
    return requests.post(
        "http://localhost:1337/api/okns",
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {jwt}"},
        data=json.dumps(
            {
                "data": full_okn
            }
        ),
    )


with open('valid_geojson_objects2.json', encoding="utf8") as f:
    okn_objects = json.loads(f.read())
    for okn_object in okn_objects:
        response = post_to_strapi(okn_object)
