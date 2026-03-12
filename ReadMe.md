# Site Alert Service - wip

Watches websites for changes, i.e. new products.
Currently configured to watch for new Mini Gt releases on SoundLimited.

Docs / Endpoints - http://127.0.0.1:5003/docs/

To Run:

1. `python -m venv venv`
2. `pip install -r requirements.txt`
3. run `python main.py` and an API will be available.

Background schedulers will run based on the task.json:

```
[
    {
        "name": "Sounds Limited",
        "slug": "sounds-limited",
        "frequeny": "hour",
        "interval": 1,
        "base_url":"https://soundslimited.co.za",
        "tasks": [
            {
                "route": "",
                "xpath": "//a[contains(@class,'product')]/@href",
                "filters": ["Mini GT", "minigt", "mini-gt", "pop race", "pop-race", "poprace", "Pop Race"] // Will only match and ping on these strings.
            }
        ]
    },
        {
        "name": "Mini GT",
        "slug": "mini-gt",
        "frequeny": "hour",
        "interval": 1,
        "base_url":"https://minigt.tsm-models.com",
        "tasks": [
            {
                "route": "index.php?action=product-list&b_id=13&p=1",
                "xpath": "//a[contains(@class,'font-weight-bold')]/text()",
                "filters": [] // Empty array will ping for any new stock
            }
        ]
    }
]
```
