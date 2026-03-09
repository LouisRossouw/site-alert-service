# Site Alert Service - wip

Watches websites for changes, i.e. new products.
Currently configured to watch for new Mini Gt releases on SoundLimited.

Docs / Endpoints - http://127.0.0.1:5003/docs/

To Run:
1. `python -m venv venv`
2. `pip install -r requirements.txt`
3. run `python main.py` and an API will be available.

Background schedulers will run based on the task.json:

`
[
    {
        "name": "Web site name",
        "slug": "web-site-name,
        "frequeny": "hour", // second, minute, hour, day
        "interval": 1,
        "base_url":"https://site.com",
        "tasks": [
            {
                "route": "", // https://www.site.com/some/route/here
                "contains": "product", // search for product in the href
                "get_element_type": "href",
                "strings_to_match": ["Mini GT", "minigt", "mini-gt", "pop race", "pop-race", "poprace", "Pop Race"]
            }
        ]
    }
]
`
