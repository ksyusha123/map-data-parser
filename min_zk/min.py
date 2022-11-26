import re

import requests
import json

from osm_requests import get_osm_info_by_parsed_address


def get_house_ids():
    url = "https://dom.mingkh.ru/sverdlovskaya-oblast/ekaterinburg/houses?page="
    links = []
    for i in range(1, 90):
        response = requests.get(f'{url}{i}')
        index = 0
        content_string = response.content.decode()

        while content_string.find("<a href=", index + 12) != -1:
            index = content_string.find("<a href=", index + 12)
            end_index = content_string.find(">", index)
            link = content_string[index + 9:end_index - 1]
            if link.find("sverdlovskaya") != -1 and link.find("houses") == -1:
                links.append(link)

    with open("minIds", 'w', encoding='utf-8') as file:
        for i in links:
            file.write(i + '\n')


def get_house_data_from_site():
    with open("minIdsRes.json", encoding='utf-8') as f:
        list_d = []
        k = 1
        for line in f:
            url = "https://dom.mingkh.ru" + line[:len(line) - 1]
            response = requests.get(f'{url}')
            if response.status_code != 200:
                print("Error" + line)
                continue
            content_string = response.content.decode()
            d = {}

            match = re.search(r'<dt>(Адрес)</dt> <dd>(.+?)<a|</dd>', content_string)
            if match:
                d[match[1]] = match[2].replace('&nbsp;&nbsp;&nbsp;', '')
            match = re.search(r'<dt>(Год постройки)</dt> <dd>(.+?)</dd>', content_string)
            if match:
                d[match[1]] = match[2].strip()
            match = re.search(r'<dt>(Количество этажей)</dt> <dd>(.+?)</dd>', content_string)
            if match:
                d[match[1]] = match[2].strip()
            match = re.search(r'<dt>(Дом признан аварийным)</dt> <dd>(.+?)</dd>', content_string)
            if match:
                d[match[1]] = match[2].strip()
            match = re.search(r'<dt>(Управляющая компания)</dt> <dd>.+?>(.+?)</span>', content_string)
            if match:
                d[match[1]] = match[2].strip()
            match = re.search(r'<dt>(Серия, тип постройки)</dt> <dd>(.+?)</dd>', content_string)
            if match:
                d[match[1]] = match[2].strip()
            match = re.search(r'<td.+?>(Износ здания, %)</td> <td .+?>(.+?)</td>', content_string)
            if match:
                d[match[1]] = match[2].strip()
            match = re.search(r'<td.+?>(Состояние дома)</td> <td .+?>(.+?)</td>', content_string)
            if match:
                d[match[1]] = match[2].strip()
            list_d.append(d)
            print(k)
            k += 1
        with open("minIdsRes", 'a', encoding='utf-8') as file:
            file.write(json.dumps(list_d, indent=4).encode('latin-1').decode(
                'unicode_escape'))


def get_data_from_osm_and_write_to_files():
    k=1
    geojson_objects = []
    geojson_objects_fail = []
    geojson_objects_not_found = []
    geojson_objects_many = []
    with open("geojson_objects_not_found.json", encoding='utf-8') as file:
        all_houses = json.load(file)
        for house in all_houses:
            ad = house["Адрес"].split(',')
            street = ad[0]
            house_number = ad[1]
            if ad[0].startswith("п.") or ad[0].startswith("с."):
                street = ad[1]
                house_number = ad[2]
            house_number = house_number.replace('48 корпус Г', '48Г')
            house_number = house_number.replace('Строение', '')
            house_number = house_number.replace('Сооружение', '')
            house_number = house_number.replace('52 корпус ', '52/')
            house_number = house_number.replace('240 корпус ', '240/')
            house_number = house_number.replace('корпус ', 'к')
            street = street.replace('б-р', 'бульвар')
            street = street.replace('мкр.', 'микрорайон')
            street = street.replace('Агриппины ', '')
            street = street.replace('Аркадия ', '')
            street = street.replace('Фонвизина пер. ', 'ул. Фонвизина')
            street = street.replace(' п-ов', '')
            street = street.replace('Буторина пер.', 'Буторина')
            street = street.replace('Василия Еремина', 'Еремина')
            street = street.replace('Многостаночников пер.', 'Многостаночников')
            street = street.replace('ул. Верещагина', 'переулок Верещагина')
            street = street.replace('ул. Культуры', 'бульвар Культуры')
            street = street.replace('ст. ', '')
            street = street.replace('пр-кт', 'проспект')
            osm_info = get_osm_info_by_parsed_address("Екатеринбург", street, house_number)
            object_features = osm_info['features']

            if len(object_features) == 0:
                geojson_objects_not_found.append(house)

            elif len(object_features) == 1:
                add_info(geojson_objects, geojson_objects_fail, house, object_features[0])

            else:
                is_many = False
                for feature in object_features:
                    if feature["properties"]["category"] == "building" or feature["properties"]["category"] == "apartments":
                        add_info(geojson_objects, geojson_objects_fail, house, feature)
                        is_many = True
                        break
                if not is_many:
                    geojson_objects_many.append(house)
            print(k)
            k+=1

    with open('geojson_objects2.json', 'w', encoding='utf-8') as file:
        string_object = json.dumps(geojson_objects, indent=4)
        string_object = string_object.encode('latin-1').decode(
            'unicode_escape')
        file.write(string_object)

    with open('geojson_objects_fail.json', 'w', encoding='utf-8') as file:
        string_object = json.dumps(geojson_objects_fail, indent=4)
        string_object = string_object.encode('latin-1').decode(
            'unicode_escape')
        file.write(string_object)

    with open('geojson_objects_many2.json', 'w', encoding='utf-8') as file:
        string_object = json.dumps(geojson_objects_many, indent=4)
        string_object = string_object.encode('latin-1').decode(
            'unicode_escape')
        file.write(string_object)

    with open('geojson_objects_not_found2.json', 'w', encoding='utf-8') as file:
        string_object = json.dumps(geojson_objects_not_found, indent=4)
        string_object = string_object.encode('latin-1').decode(
            'unicode_escape')
        file.write(string_object)


def add_info(geojson_objects, geojson_objects_fail, house, object_feature):
    try:
        if "Адрес" in house.keys():
            object_feature['Адрес'] = house["Адрес"]
        if "Год постройки" in house.keys():
            object_feature['Год постройки'] = house["Год постройки"]
        if "Количество этажей" in house.keys():
            object_feature['Количество этажей'] = house["Количество этажей"]
        if "Дом признан аварийным" in house.keys():
            object_feature['Дом признан аварийным'] = house["Дом признан аварийным"]
        if "Управляющая компания" in house.keys():
            object_feature['Управляющая компания'] = house["Управляющая компания"]
        if "Серия, тип постройки" in house.keys():
            object_feature['Серия, тип постройки'] = house["Серия, тип постройки"]
        if "Износ здания, %" in house.keys():
            object_feature['Износ здания, %'] = house["Износ здания, %"]
        if "Состояние дома" in house.keys():
            object_feature['Состояние дома'] = house["Состояние дома"]
        geojson_objects.append(object_feature)
    except:
        print("fail in add info")
        geojson_objects_fail.append(house)
