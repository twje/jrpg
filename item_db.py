import json


with open("defs/item_db.json", "r") as fp:
    data = json.load(fp)
    empty_item = data[0]
    items_db = data[1:]


def does_item_have_stats(item):
    return item["type"] in (
        "weapon",
        "accessory",
        "armor"
    )


def fill_in_missing_stats():
    for index, item in enumerate(items_db):
        item["id"] = index
        
        if not does_item_have_stats(item):
            continue

        stats = item.get("stats", {})
        for key, value in empty_item["stats"].items():
            stats[key] = stats.get(key, value)
        item["stats"] = stats        


fill_in_missing_stats()
