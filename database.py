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


def get_steamid(user_id):

    # Retrieve user binding from the database
    cursor = connection.cursor()
    connection.select_db('discord')
    cursor.execute(
        'SELECT steamid_32 FROM users WHERE discord_id = %s',
        (user_id,)
    )
    result = cursor.fetchone()
    cursor.close()

    if result:
        return result
    else:
        return


def get_join_date():
    pass
