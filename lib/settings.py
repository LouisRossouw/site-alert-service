import os
from lib.utils import read_json, write_to_json


class Settings():
    def __init__(self):
        self.root_path = os.path.dirname(os.path.dirname(__file__))
        self.configs_dir = os.path.join(self.root_path, "configs")
        self.data_dir = os.path.join(self.root_path, "data")

        self.config_path = os.path.join(self.configs_dir, "config.json")  # nopep8
        self.tasks_path = os.path.join(self.configs_dir, "tasks.json")  # nopep8
        self.results_path = os.path.join(self.data_dir, "results.json")  # nopep8

        self.config = read_json(self.config_path)
        self.tasks = read_json(self.tasks_path)

        self.name = self.config.get("name")
        self.slug = self.config.get("slug")
        self.host = self.config.get("host")
        self.port = self.config.get("port")

        self.service_path = os.path.join(self.data_dir,  f"{self.slug.replace('-', '_')}.json")  # nopep8

        self.log_file = os.path.join(
            self.root_path, "data", self.config.get("log_file"))

        self.notify_bot = self.config.get("notify_bot")
        self.notifications = self.config.get("notifications")
        self.tele_jam_api_baseurl = self.config.get("tele_jam_api_baseurl")

    def get_logs(self, lines=20):
        if not os.path.exists(self.log_file):
            return "No logs yet."

        with open(self.log_file, "r") as f:
            return "".join(f.readlines()[-lines:])

    def get_config(self):
        return read_json(self.config_path)

    def update_config(self, data):
        write_to_json(self.config_path, data)
        return self.reload()

    def get_setting(self, key):
        return read_json(self.config_path).get(key)

    def get_tasks(self):
        return read_json(self.tasks_path)

    def update_tasks(self, data):
        return write_to_json(self.tasks_path, data)

    def reload(self):
        self.config = read_json(self.config_path)
        self.tasks = read_json(self.tasks_path)
        self.results = read_json(self.results_path)

        self.name = self.config.get("name")
        self.slug = self.config.get("slug")
        self.host = self.config.get("host")
        self.port = self.config.get("port")

        self.service_path = os.path.join(self.data_dir,  f"{self.slug.replace('-', '_')}.json")  # nopep8

        self.log_file = os.path.join(
            self.root_path, "data", self.config.get("log_file"))

        self.notify_bot = self.config.get("notify_bot")
        self.notifications = self.config.get("notifications")
        self.tele_jam_api_baseurl = self.config.get("tele_jam_api_baseurl")
