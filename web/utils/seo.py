from web.utils.helper import get

meta_data = {
    "title": "uPaty",
    "wtti": "uPaty",
    "keywords": "uPaty",
    "description": "uPaty is the best way to help you plan your party",
    "image": ""
}

def updateMetaData(**kwargs):
    meta_data["title"] = get(kwargs, "title", "")
    meta_data["wtti"] = get(kwargs, "wtti", "")
    meta_data["keywords"] = get(kwargs, "keywords", "")
    meta_data["description"] = get(kwargs, "description", "")
    meta_data["image"] = get(kwargs, "image", "")
