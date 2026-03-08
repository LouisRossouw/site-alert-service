import json
import requests


def write_to_json(json_path, data):
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=6)


def read_json(json_path):
    with open(json_path) as f:
        json_file = json.loads(f.read())

    return (json_file)


def is_internet_available():
    try:
        response = requests.get("http://www.google.com", timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        pass
    return False
