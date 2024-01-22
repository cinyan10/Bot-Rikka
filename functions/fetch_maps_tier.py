from functions.query import *
f = open('../maps.txt', 'r', encoding='utf-8')
maps = []
for line in f.readlines():
    map_name = line.strip().split('.')[0]
    maps.append(map_name)

f.close()
print(len(maps))

maps_tier = {}
count = 0
for m in maps:
    tier = fetch_map_tier(m)
    maps_tier[m] = tier
    count += 1
    print('added', m, count, '/', 957)

print(maps_tier)

w = open('../files/maps_tier.json', 'w', encoding='utf-8')
w.write(json.dumps(maps_tier))
w.close()

