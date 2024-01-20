from query import *
content = '北京1'

try:
    num = int(content)
    print(num)
    query_csgo_server(servers[num][0], servers[num][1])
except Exception:
    if content[:1] == '北京':
        num = int(content[2]) + 6
        print(num)
        query_csgo_server(servers[num][0], servers[num][1])
    elif content[:1] == '广州':
        num = int(content[2])
        print(num)
        query_csgo_server(servers[num][0], servers[num][1])

