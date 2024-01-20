from query import *
content = '北京1'
num = 0
try:
    num = int(content)
    print(num)
    query_csgo_server(servers[num][0], servers[num][1])
except Exception:
    if content[:2] == '北京':
        num = int(content[2]) + 6
        print(num)
        query_csgo_server(servers[num][0], servers[num][1])
    elif content[:2] == '广州':
        num = int(content[2])
        print(num)
        query_csgo_server(servers[num][0], servers[num][1])



