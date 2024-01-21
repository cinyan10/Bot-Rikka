import json
with open('maps.json', 'r', encoding='utf-8') as file:
    data_str = file.read().strip()
    maps = json.loads(data_str)

    map_tiers = {}
    for m in maps:
        map_tiers[m['name']] = m['difficulty']


