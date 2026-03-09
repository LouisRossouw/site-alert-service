import os
import logging
import requests
from lxml import html
from datetime import datetime
from logging.handlers import RotatingFileHandler

from lib.utils import read_json, write_to_json, is_internet_available


this_dir = os.path.dirname(__file__)

handler = RotatingFileHandler(
    "data/service.log", maxBytes=1_000_000, backupCount=3)

logging.basicConfig(
    handlers=[handler],
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def get_tasks(web_task):
    results = []
    for task in web_task.get("tasks"):
        result, string = get_element(web_task.get("base_url"), task)

        date_now = datetime.now()

        if result:
            results.append({
                "datetime": date_now.strftime("%d-%m-%Y %H:%M"),
                "timestamp": date_now.timestamp(),
                "result": result,
                "matched_string": string,
                **task
            })

    return results


def get_element(base_url, task):
    res = requests.get(f"{base_url}/{task.get('route')}")
    tree = html.fromstring(res.content)

    strings_to_match = task.get("strings_to_match")
    element_type = task.get("get_element_type")
    contains = task.get("contains")

    if element_type == "href":
        href = tree.xpath(f'//a[contains(@class,"{contains}")]')[0].get("href")

        for string in strings_to_match:
            if str(string).lower() in str(href).lower():
                return href, string
    return None, ''


def check_if_diff(last_results, results):
    if len(results) <= 0:
        return []

    differences = []

    for i in range(len(last_results)):
        prev_slug = last_results[i].get('slug')
        prev_result = last_results[i].get('result')

        result = results[i].get('result')
        slug = results[i].get('slug')

        if prev_slug == slug:
            if prev_result != result:
                differences.append(results[i])

    return differences


def format_alert(data):
    return (
        f"🌐 {data.get('name')} - {data.get('base_url')}\n\n"
        f"🛒 New {data.get('matched_string')}\n\n"
        f"🔗 {data.get('result')}\n\v"
    )


def run(settings, web_task):

    if not is_internet_available():
        logging.info("No internet connection..")
        return

    results_path = os.path.join(this_dir, settings.results_path)

    results_exists = os.path.exists(results_path)
    last_results = [] if not results_exists else read_json(results_path)

    results = get_tasks(web_task)
    differences = check_if_diff(last_results, results)

    logging.info("%s - results: %s diff: %s", settings.name,
                 len(results), len(differences))

    formatted_txts = []
    if differences:
        for diff in differences:
            formatted_txts.append(format_alert(diff))

        payload = [f"🏎️ {settings.name}:\n\n"]
        for f in formatted_txts:
            payload.append(f)

        # Alert the user via Telegram.
        if settings.notifications:
            url = f"{settings.tele_jam_api_baseurl}/notify/bots/{settings.notify_bot}"
            requests.post(url=url, json=payload)

    # Update recorded results
    write_to_json(results_path, results)


if __name__ == "__main__":
    from lib.settings import Settings

    settings = Settings()
    logging.info(f"{settings.name} has started..")

    try:
        run(settings)
    except Exception as e:
        logging.exception("Something went wrong")
