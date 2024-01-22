def find_server_by_name(server_name_short):
    """find a server by short name"""
    for server in SERVER_LIST:
        if server_name_short == server.name_short:
            return server


def find_server_by_id(server_id):
    """find a server by id"""
    for server in SERVER_LIST:
        if server.id == server_id:
            return server


class Server:
    name = None

    def __str__(self):
        return f'Server: {self.name_cn}, {self.id}'
    def __init__(self, name: str, name_cn: str, name_short: str, server_id: int, ip: str, port: int):
        self.name = name
        self.name_cn = name_cn
        self.name_short = name_short
        self.id = server_id
        self.ip = ip
        self.port = port


SERVER_LIST = [
    Server('GOKZ GuangZhou #1', 'GOKZ 广州#1', '广州1', 1, '43.139.56.16', 10001),
    Server('GOKZ GuangZhou #2', 'GOKZ 广州#2', '广州2', 2, '43.139.56.16', 10002),
    Server('GOKZ GuangZhou #3', 'GOKZ 广州#3', '广州3', 3, '43.139.56.16', 10003),
    Server('GOKZ GuangZhou #4', 'GOKZ 广州#4', '广州4', 4, '43.139.56.16', 10004),
    Server('GOKZ GuangZhou #5', 'GOKZ 广州#5', '广州5', 5, '43.139.56.16', 10005),
    Server('GOKZ GuangZhou #6', 'GOKZ 广州#6', '广州6', 6, '43.139.56.16', 10006),
    Server('GOKZ BeiJing #1', 'GOKZ 北京#1', '北京1', 7, '43.138.126.94', 10001),
    Server('GOKZ BeiJing #2', 'GOKZ 北京#2', '北京2', 8, '43.138.126.94', 10002),
    Server('GOKZ BeiJing #3', 'GOKZ 北京#3', '北京3', 9, '43.138.126.94', 10003),
    Server('GOKZ BeiJing #4', 'GOKZ 北京#4', '北京4', 10, '43.138.126.94', 10004),
    Server('GOKZ BeiJing #5', 'GOKZ 北京#5', '北京5', 11, '43.138.126.94', 10005),
    Server('GOKZ BeiJing #6', 'GOKZ 北京#6', '北京6', 12, '43.138.126.94', 10006),
]


if __name__ == '__main__':
    server = SERVER_LIST[0]
    print(server.ip)
