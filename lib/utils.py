import json
import time
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


def start_time():
    """ Prints when an API is called. """
    return time.time()


def calculate_request_time(start_time):
    """ Calculates the Database queries. """
    return time.time() - start_time
