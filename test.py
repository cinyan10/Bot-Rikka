from query import *
content = '1'
num = 0
try:
    num = int(content) - 1
    query_csgo_server(servers[num][0], servers[num][1])
except Exception:
    if content[:2] == '北京':
        num = int(content[2]) + 5
        query_csgo_server(servers[num][0], servers[num][1])
    elif content[:2] == '广州':
        num = int(content[2]) - 1
        query_csgo_server(servers[num][0], servers[num][1])



