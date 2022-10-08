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


f = requests.get('https://raw.githubusercontent.com/ksyusha123/okn-parser/master/valid_geojson_objects.json')
okn_objects = f.json()
for okn_object in okn_objects:
    okn_object["geometry"]["coordinates"] = {
        "longitude": okn_object["geometry"]["coordinates"][0],
        "latitude": okn_object["geometry"]["coordinates"][1]
    }
    response = post_to_strapi(okn_object)
