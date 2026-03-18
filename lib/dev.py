
import requests
from lxml import html


def get_element(base_url, task):
    """ Returns the first matching element. """

    res = requests.get(f"{base_url}/{task.get('route')}", headers={
        "User-Agent": "Mozilla/5.0"
    })

    print("\nres code:\n", res.status_code)
    print("\nres text:\n", res.text[:1000])

    tree = html.fromstring(res.content)

    filters = task.get("filters", [])
    xpath = task.get("xpath")

    elements = tree.xpath(xpath)

    print('\nelements:\n')
    print(tree)

    if not elements:
        return None, ''

    href = elements[0] if isinstance(
        elements[0], str) else elements[0].get("href")

    if not filters:
        return href, ''

    for filter in filters:
        if filter.lower() in href.lower():
            return href.lower(), filter

    return None, ''


if __name__ == "__main__":
    result, filter = get_element(base_url="https://www.vagcafe.com/product-tag/mini-gt/", task={
        "xpath": "//a[contains(@class,'wd-entities-title')]",
        "filters": [],
        "route": "",
    })

    print('----')
    print('\nfilter:', filter)
    print('\nresult:\n', result)
    print('----')
