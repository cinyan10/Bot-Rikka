import json
import requests


def fetching_maps(use_local=False):
    if use_local:
        with open('maps.json', 'r', encoding='utf-8') as json_file:
            maps_data = json.load(json_file)
    else:
        api_url = "https://kztimerglobal.com/api/v2.0/maps?is_validated=true&limit=2000"
        response = requests.get(api_url)
        response.raise_for_status()
        maps_data = response.json()
        with open('maps.json', 'w', encoding="utf-8") as json_file:
            json.dump(maps_data, json_file)

    return maps_data


def get_map_tier(map_name=None, id=None):
    maps_data = fetching_maps()
    if map_name is not None:
        for map in maps_data:
            if map['name'] == map_name:
                return map['difficulty']
    elif id is not None:
        for map in maps_data:
            if map['id'] == id:
                return map['difficulty']


if __name__ == '__main__':
    tier = get_map_tier(id=842)
    print(tier)
    pass
