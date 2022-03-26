import json


def write_json_file(file, json_object):
    dumped_object = json.dumps(json_object, indent=4)
    with open(file, "w", encoding="utf8") as outfile:
        outfile.write(dumped_object)


def read_json_file(file):
    with open(file, "r", encoding="utf8") as readfile:
        json_object = json.loads(readfile.read())

    return json_object
