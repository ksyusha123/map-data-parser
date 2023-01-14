import hashlib
import re

import requests
import json

from osm_requests import get_osm_info_by_parsed_address
from strapi_requests import get_object, put_object

url = 'http://51.178.191.76:1337'


def get_house_ids():
    url = "https://domaekb.ru/poisk?page="
    links = []
    for i in range(0, 171):
        response = requests.get(f'{url}{i}')
        index = 0
        content_string = response.content.decode()

        while content_string.find("<a href=", index + 12) != -1:
            index = content_string.find("<a href=", index + 12)
            end_index = content_string.find(">", index)
            link = content_string[index + 9:end_index - 1]
            if link.find("dom") != -1:
                links.append(link)

    with open("minIds2", 'w', encoding='utf-8') as file:
        for i in links:
            file.write(i + '\n')


def get_house_data_from_site():
    with open("C:\\Users\\79022\\map-data-parser\\min_zk\\minIdsRes2", encoding='utf-8') as f:
        list_d = []
        k = 1
        for line in f:
            url = "https://domaekb.ru" + line[:len(line) - 1]
            response = requests.get(f'{url}')
            if response.status_code != 200:
                print("Error" + line)
                continue
            content_string = response.content.decode()
            d = {}

            match = re.search(r'(Адрес дома:)&nbsp;<\/div>.+?field-item even">(.+?)<\/div>', content_string)
            if match:
                d[match[1]] = match[2].replace('&nbsp;', '')
            match = re.search(r'(Год постройки:)&nbsp;<\/div>.+?field-item even">(.+?)<\/div>', content_string)
            if match:
                d[match[1]] = match[2].replace('&nbsp;', '')
            match = re.search(r'(Факт признания дома аварийным:)&nbsp;<\/div>.+?field-item even">(.+?)<\/div>',
                              content_string)
            if match:
                d[match[1]] = match[2].replace('&nbsp;', '')
            match = re.search(r'(Наибольшее количество этажей, ед\.:)&nbsp;<\/div>.+?field-item even">(.+?)<\/div>',
                              content_string)
            if match:
                d[match[1]] = match[2].replace('&nbsp;', '')
            match = re.search(r'(Наименьшее количество этажей, ед\.:)&nbsp;<\/div>.+?field-item even">(.+?)<\/div>',
                              content_string)
            if match:
                d[match[1]] = match[2].replace('&nbsp;', '')
            match = re.search(r'(Управляющая компания:)&nbsp;</div> .+?<a href .+?>(.+?)</a>', content_string)
            if match:
                d[match[1]] = match[2].replace('&nbsp;', '')
            match = re.search(r'(Серия, тип постройки здания:)&nbsp;<\/div>.+?field-item even">(.+?)<\/div>',
                              content_string)
            if match:
                d[match[1]] = match[2].replace('&nbsp;', '')
            match = re.search(r'(Количество подъездов, ед\.:)&nbsp;<\/div>.+?field-item even">(.+?)<\/div>',
                              content_string)
            if match:
                d[match[1]] = match[2].replace('&nbsp;', '')
            match = re.search(r'(Количество лифтов, ед\.:)&nbsp;<\/div>.+?field-item even">(.+?)<\/div>',
                              content_string)
            if match:
                d[match[1]] = match[2].replace('&nbsp;', '')
            match = re.search(r'(Количество помещений, всего, ед\.:)&nbsp;<\/div>.+?field-item even">(.+?)<\/div>',
                              content_string)
            if match:
                d[match[1]] = match[2].replace('&nbsp;', '')
            match = re.search(r'(Количество жилых помещений, ед\.:)&nbsp;<\/div>.+?field-item even">(.+?)<\/div>',
                              content_string)
            if match:
                d[match[1]] = match[2].replace('&nbsp;', '')
            list_d.append(d)
            print(k)
            k += 1
        with open("C:\\Users\\79022\\map-data-parser\\min_zk\\minIdsRes2", 'a', encoding='utf-8') as file:
            file.write(json.dumps(list_d, indent=4).encode('latin-1').decode(
                'unicode_escape'))


def get_data_from_osm_and_write_to_files():
    k = 1
    geojson_objects = []
    geojson_objects_fail = []
    geojson_objects_not_found = []
    geojson_objects_many = []
    with open("C:\\Users\\79022\\map-data-parser\\min_zk\\minIdsRes4", encoding='utf-8') as file:
        all_houses = json.load(file)
        for house in all_houses:
            try:
                ad = house["Адрес дома:"].split(',')
                street = ad[1].strip()
                house_number = ad[2].strip()
                if ad[1].startswith("п.") or ad[1].startswith("с."):
                    street = ad[2].strip()
                    house_number = ad[3].strip()
                # house_number = house_number.replace('48 корпус Г', '48Г')
                house_number = house_number.replace('Строение', '')
                house_number = house_number.replace('Сооружение', '')
                # house_number = house_number.replace('52 корпус ', '52/')
                # house_number = house_number.replace('240 корпус ', '240/')
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
                        if feature["properties"]["category"] == "building" or feature["properties"][
                            "category"] == "apartments":
                            add_info(geojson_objects, geojson_objects_fail, house, feature)
                            is_many = True
                            break
                    if not is_many:
                        geojson_objects_many.append(house)
                print(k)
                k += 1
            except:
                geojson_objects_fail.append(house)

    with open('geojson_objects_182_12.json', 'w', encoding='utf-8') as file:
        string_object = json.dumps(geojson_objects, indent=4)
        string_object = string_object.encode('latin-1').decode(
            'unicode_escape')
        file.write(string_object)

    with open('geojson_objects_fail_182_12.json', 'w', encoding='utf-8') as file:
        string_object = json.dumps(geojson_objects_fail, indent=4)
        string_object = string_object.encode('latin-1').decode(
            'unicode_escape')
        file.write(string_object)

    with open('geojson_objects_many_182_12.json', 'w', encoding='utf-8') as file:
        string_object = json.dumps(geojson_objects_many, indent=4)
        string_object = string_object.encode('latin-1').decode(
            'unicode_escape')
        file.write(string_object)

    with open('geojson_objects_not_found_182_12.json', 'w', encoding='utf-8') as file:
        string_object = json.dumps(geojson_objects_not_found, indent=4)
        string_object = string_object.encode('latin-1').decode(
            'unicode_escape')
        file.write(string_object)


def add_info(geojson_objects, geojson_objects_fail, house, object_feature):
    try:
        if "Адрес дома:" in house.keys():
            object_feature['Адрес'] = house["Адрес дома:"]
        if "Год постройки:" in house.keys():
            object_feature['Год постройки'] = house["Год постройки:"]
        if "Наибольшее количество этажей, ед.:" in house.keys():
            object_feature['Количество этажей'] = house["Наибольшее количество этажей, ед.:"]
        if "Наименьшее количество этажей, ед.:" in house.keys():
            object_feature['Наименьшее количество этажей'] = house["Наименьшее количество этажей, ед.:"]
        if "Факт признания дома аварийным:" in house.keys():
            object_feature['Дом признан аварийным'] = house["Факт признания дома аварийным:"]
        if "Управляющая компания" in house.keys():
            object_feature['Управляющая компания'] = house["Управляющая компания"]
        if "Серия, тип постройки здания:" in house.keys():
            object_feature['Серия, тип постройки'] = house["Серия, тип постройки здания:"]
        if "Износ здания, %" in house.keys():
            object_feature['Износ здания, %'] = house["Износ здания, %"]
        if "Состояние дома" in house.keys():
            object_feature['Состояние дома'] = house["Состояние дома"]

        if "Количество подъездов, ед.:" in house.keys():
            object_feature['Количество подъездов'] = house["Количество подъездов, ед.:"]
        if "Количество лифтов, ед.:" in house.keys():
            object_feature['Количество лифтов'] = house["Количество лифтов, ед.:"]
        if "Количество помещений, всего, ед.:" in house.keys():
            object_feature['Количество помещений'] = house["Количество помещений, всего, ед.:"]
        if "Количество жилых помещений, ед.:" in house.keys():
            object_feature['Количество жилых помещений'] = house["Количество жилых помещений, ед.:"]
        geojson_objects.append(object_feature)
    except:
        print("fail in add info")
        geojson_objects_fail.append(house)


def add_geo():
    with open('C:\\Users\\79022\\map-data-parser\\min_zk\\center.json', 'r', encoding='utf-8') as constructions:
        with open('C:\\Users\\79022\\map-data-parser\\only1.json', 'r', encoding='utf-8') as only:
            const_json = json.load(constructions).values()
            only_json = json.load(only)
            for only in only_json:
                for con in const_json:
                    if only['id'] == con['id']:
                        only['geometry'] = con['geometry']

        with open('only1_new.json', 'w', encoding='utf-8') as file:
            string_object = json.dumps(only_json, indent=4)
            string_object = string_object.encode('latin-1').decode(
                'unicode_escape')
            file.write(string_object)


def floors():
    err_json = []
    only_json = []
    ex_json = []
    ok_json = []
    with open('C:\\Users\\79022\\map-data-parser\\api-center-construction.json', 'r',
              encoding='utf-8') as constructions:
        const_json = json.load(constructions).values()
        for c_json in const_json:
            for i in range(1, 19):
                with open(f'C:\\Users\\79022\\map-data-parser\\min_zk\\geojson_objects{i}.json', 'r',
                          encoding='utf-8') as min_zkh:
                    min_zkh_json = json.load(min_zkh)
                    for m_obj in min_zkh_json:
                        try:
                            if c_json['street'] is not None and m_obj['Address'] is not None and c_json[
                                'house_number'] is not None and m_obj['Address'] is not None:
                                if c_json['street'] in m_obj['Address'] and c_json['house_number'] in m_obj['Address']:
                                    if c_json['floors'] is not None and m_obj['Floors'] is not None:
                                        if c_json['floors'] == int(m_obj['Floors']):
                                            ok_json.append(m_obj)
                                        else:
                                            err_json.append(m_obj)
                                    elif c_json['floors'] is not None:
                                        ok_json.append(c_json)
                                    elif m_obj['Floors'] is not None:
                                        ok_json.append(m_obj)
                                else:
                                    if i == 18:
                                        only_json.append(c_json)
                        except:
                            ex_json.append(m_obj)
                            continue
        with open('ok.json', 'w', encoding='utf-8') as file:
            string_object = json.dumps(ok_json, indent=4)
            string_object = string_object.encode('latin-1').decode(
                'unicode_escape')
            file.write(string_object)

        with open('err.json', 'w', encoding='utf-8') as file:
            string_object = json.dumps(err_json, indent=4)
            string_object = string_object.encode('latin-1').decode(
                'unicode_escape')
            file.write(string_object)

        with open('ex.json', 'w', encoding='utf-8') as file:
            string_object = json.dumps(ex_json, indent=4)
            string_object = string_object.encode('latin-1').decode(
                'unicode_escape')
            file.write(string_object)

        with open('only.json', 'w', encoding='utf-8') as file:
            string_object = json.dumps(only_json, indent=4)
            string_object = string_object.encode('latin-1').decode(
                'unicode_escape')
            file.write(string_object)


def add_new():
    token = ""
    with open('C:\\Users\\79022\\map-data-parser\\geojson_objects_182_12.json', encoding='utf-8') as file:
        all_data = json.load(file)
        for data in all_data:
            try:
                str_coordinates = ','.join(map(str, data['geometry']['coordinates']))
                current_hash = hashlib.md5(bytes(str_coordinates, 'utf-8')).hexdigest()
                res = get_object(token, current_hash)
                if len(res['results']) == 1:
                    # if 'Количество жилых помещений, ед.:' in dataF and dataF['Количество жилых помещений, ед.:']:
                    #     res['results'][0]['LivingRoomsCount'] = dataF['Количество жилых помещений, ед.:']
                    # if 'Количество помещений, всего, ед.:' in dataF and dataF['Количество помещений, всего, ед.:']:
                    #     res['results'][0]['RoomsCount'] = dataF['Количество помещений, всего, ед.:']
                    # if 'Количество лифтов, ед.:' in dataF and dataF['Количество лифтов, ед.:']:
                    #     res['results'][0]['LiftsCount'] = dataF['Количество лифтов, ед.:']
                    # if 'Количество подъездов, ед.:' in dataF and dataF['Количество подъездов, ед.:']:
                    #     res['results'][0]['EntranceCount'] = dataF['Количество подъездов, ед.:']
                    # if 'Наименьшее количество этажей, ед.:' in dataF and dataF['Наименьшее количество этажей, ед.:']:
                    #     res['results'][0]['MinimalFloors'] = dataF['Наименьшее количество этажей, ед.:']
                    # if 'Серия, тип постройки здания:' in dataF and dataF['Серия, тип постройки здания:']:
                    #     res['results'][0]['Series'] = dataF['Серия, тип постройки здания:']
                    # if 'Наибольшее количество этажей, ед.:' in dataF and dataF['Наибольшее количество этажей, ед.:']:
                    #     res['results'][0]['Floors'] = dataF['Наибольшее количество этажей, ед.:']
                    # if 'Факт признания дома аварийным:' in dataF and dataF['Факт признания дома аварийным:']:
                    #     res['results'][0]['Emergency'] = dataF['Факт признания дома аварийным:']
                    # if 'Год постройки:' in dataF and dataF['Год постройки:']:
                    #     res['results'][0]['Year'] = dataF['Год постройки:']
                    # if 'Адрес дома:' in dataF and dataF['Адрес дома:']:
                    #     res['results'][0]['Address'] = dataF['Адрес дома:']
                    # put_object(token, res['results'][0], res['results'][0]['id'])
                    # break
                    if 'LivingRoomsCount' in data and data['LivingRoomsCount']:
                        res['results'][0]['LivingRoomsCount'] = data['LivingRoomsCount']
                    if 'RoomsCount' in data and data['RoomsCount']:
                        res['results'][0]['RoomsCount'] = data['RoomsCount']
                    if 'LiftsCount' in data and data['LiftsCount']:
                        res['results'][0]['LiftsCount'] = data['LiftsCount']
                    if 'EntranceCount' in data and data['EntranceCount']:
                        res['results'][0]['EntranceCount'] = data['EntranceCount']
                    if 'MinimalFloors' in data and data['MinimalFloors']:
                        res['results'][0]['MinimalFloors'] = data['MinimalFloors']
                    put_object(token, res['results'][0], res['results'][0]['id'])
            except:
                print(data)
                continue
