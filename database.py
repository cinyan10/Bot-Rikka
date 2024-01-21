import os
from pymysql import Connection
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
host = os.getenv('MYSQL_HOST')
port = os.getenv('MYSQL_PORT')
password = os.getenv('MYSQL_PASSWORD')

connection = Connection(
    host=host,
    port=int(port),
    user="root",
    password=password,
)

