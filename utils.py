import json


def write_to_json(json_path, data):
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=6)


def read_json(json_path):
    with open(json_path) as f:
        json_file = json.loads(f.read())

    return (json_file)
