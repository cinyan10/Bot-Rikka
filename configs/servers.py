from functions.db_operate.sourceban import query_sb_servers
from functions.server import Server

SERVERS = query_sb_servers()

SERVER_LIST = [
    Server('GOKZ GuangZhou #1', 'GOKZ 广州#1', '广州1', 1, '43.139.56.16', 10001, 1200514677495570544),
    Server('GOKZ GuangZhou #2', 'GOKZ 广州#2', '广州2', 2, '43.139.56.16', 10002, 1200514715697287178),
    Server('GOKZ GuangZhou #3', 'GOKZ 广州#3', '广州3', 3, '43.139.56.16', 10003, 1200514743773954058),
    Server('GOKZ GuangZhou #4', 'GOKZ 广州#4', '广州4', 4, '43.139.56.16', 10004, 1200514782751641781),
    Server('GOKZ GuangZhou #5', 'GOKZ 广州#5', '广州5', 5, '43.139.56.16', 10005, 1200514805237301280),
    Server('GOKZ GuangZhou #6', 'GOKZ 广州#6', '广州6', 6, '43.139.56.16', 10006, 1200514845506818220),
    Server('GOKZ BeiJing #1', 'GOKZ 北京#1', '北京1', 7, '43.138.126.94', 10001, 1200514868629999756),
    Server('GOKZ BeiJing #2', 'GOKZ 北京#2', '北京2', 8, '43.138.126.94', 10002, 1200514889437941930),
    Server('GOKZ BeiJing #3', 'GOKZ 北京#3', '北京3', 9, '43.138.126.94', 10003, 1200514912703754360),
    Server('GOKZ BeiJing #4', 'GOKZ 北京#4', '北京4', 10, '43.138.126.94', 10004, 1200514930315640905),
    Server('GOKZ BeiJing #5', 'GOKZ 北京#5', '北京5', 11, '43.138.126.94', 10005, 1200514949554913342),
    Server('GOKZ BeiJing #6', 'GOKZ 北京#6', '北京6', 12, '43.138.126.94', 10006, 1200514970543198318),
]
