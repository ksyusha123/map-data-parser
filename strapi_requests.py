import os

import requests

url = 'http://51.178.191.76:1337'


def post_new_dtp_object(bearer: str, data: str) -> dict:
    headers = dict([
        ('Accept', 'application/json'),
        ('Accept-Language', 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7'),
        ('Authorization', f'Bearer {bearer}'),
        ('Cache-Control', 'no-cache'),
        ('Connection', 'keep-alive'),
        ('Content-Type', 'application/json'),
        ('Origin', 'http://51.178.191.76:1337'),
        ('Pragma', 'no-cache'),
        ('User-Agent',
         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.56')
    ])
    response = requests.post(f'http://51.178.191.76:1337/api/dtps', json={"data": data},
                             headers=headers)
    return response.json()


def strapi_login():
    data = {
        "identifier": os.environ.get('MAP-USER-LOGIN'),
        "password": os.environ.get('MAP-USER-PASSWORD')
    }
    response = requests.post(f'{url}/api/auth/local', json=data)
    return response.json()
