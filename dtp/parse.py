import json


def parse_dtp():
    count = 1
    object_to_file = []
    object_without_address = []
    file_path = ''
    with open(file_path, encoding='utf-8') as file:
        all_dtps = json.load(file)['features']
        for dtp in all_dtps:
            if not(dtp["properties"]["region"] is None):
                if "Екатеринбург" in dtp["properties"]["region"]:
                    dtp_obj = {}
                    dtp_obj = dtp['properties']
                    dtp_obj['geometry'] = dtp['geometry']
                    object_to_file.append(dtp_obj)
            else:
                object_without_address.append(dtp)
            if len(object_to_file) == 300:
                with open(f"dtp_ekb_{count}.json", 'w', encoding='utf-8') as file_to_write:
                    string_object = json.dumps(object_to_file, indent=4)
                    string_object = string_object.encode('latin-1').decode(
                        'unicode_escape')
                    file_to_write.write(string_object)
                object_to_file = []
                count+=1
        with open(f"dtp_ekb_{count}.json", 'w', encoding='utf-8') as file_to_write:
            string_object = json.dumps(object_to_file, indent=4)
            string_object = string_object.encode('latin-1').decode(
                'unicode_escape')
            file_to_write.write(string_object)