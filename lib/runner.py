import os
import logging
import requests
from lxml import html
from datetime import datetime
from logging.handlers import RotatingFileHandler

from lib.utils import read_json, write_to_json, is_internet_available, start_time, calculate_request_time

this_dir = os.path.dirname(__file__)

handler = RotatingFileHandler(
    "data/service.log", maxBytes=1_000_000, backupCount=3)

logging.basicConfig(
    handlers=[handler],
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def get_tasks(web_task):
    """ Returns the task """
    results = []
    for task in web_task.get("tasks"):

        st = start_time()
        date_now = datetime.now()

        result, string = get_element(web_task.get("base_url"), task)

        if result:
            results.append({
                "elapsed_time": calculate_request_time(st),
                "datetime": date_now.strftime("%d-%m-%Y %H:%M"),
                "timestamp": date_now.timestamp(),
                "result": result,
                "matched_string": string,
                **task
            })

    return results


# def get_element(base_url, task):
#     """ Returns the found href matching """
#     res = requests.get(f"{base_url}/{task.get('route')}")
#     tree = html.fromstring(res.content)

#     strings_to_match = task.get("strings_to_match")
#     element_type = task.get("get_element_type")
#     contains = task.get("contains")

#     if element_type == "href":
#         href = tree.xpath(f'//a[contains(@class,"{contains}")]')[0].get("href")

#         for string in strings_to_match:
#             if str(string).lower() in str(href).lower():
#                 return href, string
#     return None, ''
def get_element(base_url, task):
    """Returns the first matching element"""

    res = requests.get(f"{base_url}/{task.get('route')}", headers={
        "User-Agent": "Mozilla/5.0"
    })

    tree = html.fromstring(res.content)

    strings_to_match = task.get("strings_to_match", [])
    xpath = task.get("xpath")

    elements = tree.xpath(xpath)

    if not elements:
        return None, ''

    href = elements[0] if isinstance(
        elements[0], str) else elements[0].get("href")

    if not strings_to_match:
        return href, ''

    for string in strings_to_match:
        if string.lower() in href.lower():
            return href.lower(), string

    return None, ''


def check_if_diff(last_results, results):
    """ Compares prev and curr results to detect if new stock. """
    if len(results) <= 0:
        return []

    if not last_results:
        return results

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


def format_alert(web_task, data):
    """ Formats the text for telegram. """

    return (
        f"🌐 {web_task['name']} - {web_task['base_url']}\n"
        f"🛒 New {data.get('matched_string')}\n"
        f"🔗 {data.get('result')}\n\v"
    )


def run(settings, web_task):
    st = start_time()

    if not is_internet_available():
        logging.info("No internet connection..")
        return

    name = web_task['slug'].replace('-', '_')
    results_path = os.path.join(settings.data_dir, f"{name}_results.json")

    results_exists = os.path.exists(results_path)
    last_results = [] if not results_exists else read_json(results_path)

    results = get_tasks(web_task)
    differences = check_if_diff(last_results, results)

    logging.info("%s - results: %s diff: %s", settings.name,
                 len(results), len(differences))

    formatted_txts = []
    if differences:
        for diff in differences:
            formatted_txts.append(format_alert(web_task, diff))

        payload = [f"🏎️ {settings.name}:\n\n"]
        for f in formatted_txts:
            payload.append(f)

        # Alert the user via Telegram.
        if settings.notifications:
            url = f"{settings.tele_jam_api_baseurl}/notify/bots/{settings.notify_bot}"
            requests.post(url=url, json=payload)

    elapsed_time = calculate_request_time(st)

    date_now = datetime.now()
    manifest_path = os.path.join(settings.data_dir, f"{name}_manifest.json")

    data = {
        "system_name": settings.name,
        "system_slug": settings.slug,
        "elapsed_time": elapsed_time,
        "timestamp": date_now.timestamp(),
        "datetime": date_now.strftime("%d-%m-%Y %H:%M")}

    # Update recorded results - this is to compare against future results.
    write_to_json(results_path, results)

    # Manifest
    write_to_json(manifest_path, {
        **web_task,
        **data
    })

    # System
    write_to_json(settings.service_path, data)


if __name__ == "__main__":

    error_count = 0

    from lib.settings import Settings

    settings = Settings()
    logging.info(f"{settings.name} has started..")

    while True:
        try:
            run(settings)
            error_count = 0
        except Exception as e:
            logging.exception("Something went wrong")

            error_count += 1

            if error_count >= 5:
                url = f"{settings.tele_jam_api_baseurl}/notify/bots/{settings.notify_bot}"
                requests.post(url=url, json=[
                    f"🏎️ {settings.name}:\n\n",
                    f"❌Something is wrong with {settings.name}! \n\n Waiting for admin input."
                ])

                input()
