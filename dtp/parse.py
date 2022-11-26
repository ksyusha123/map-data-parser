import json


def parse_dtp():
    count = 1
    object_to_file = []
    object_without_address = []
    with open("C:\\Users\\79022\\Downloads\\sverdlovskaia-oblast (1).json", encoding='utf-8') as file:
        all_dtps = json.load(file)
        for dtp in all_dtps:
            if not(dtp["properties"]["region"] is None):
                if "Екатеринбург" in dtp["properties"]["region"]:
                    object_to_file.append(dtp)
            else:
                object_without_address.append(dtp)
            if len(object_to_file) == 250:
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

    # with open("dtp_without_address_2019.json", 'w', encoding='utf-8') as file_to_write:
    #     string_object = json.dumps(object_without_address, indent=4)
    #     string_object = string_object.encode('latin-1').decode(
    #         'unicode_escape')
    #     file_to_write.write(string_object)