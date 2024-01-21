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


def retrieve_steam_id(discord_id):
    cursor = connection.cursor()
    connection.select_db('discord')
    cursor.execute(
        'SELECT steamid_32 FROM users WHERE discord_id = %s',
        (discord_id,)
    )
    result = cursor.fetchone()
    cursor.close()

    return result[0] if result else None


def retrieve_join_date(steam_id):
    cursor = connection.cursor()
    connection.select_db('firstjoin')
    cursor.execute(
        'SELECT joindate FROM firstjoin WHERE auth = %s',
        (steam_id,)
    )
    result = cursor.fetchone()
    cursor.close()

    return result[0] if result else None


# Function to retrieve last_seen from firstjoin table by steamid
def retrieve_last_seen(steam_id):
    cursor = connection.cursor()
    connection.select_db('firstjoin')
    cursor.execute(
        'SELECT lastseen FROM firstjoin WHERE auth = %s',
        (steam_id,)
    )
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None


def reset_user_steam(discord_id, steam_id):
    cursor = connection.cursor()
    connection.select_db('discord')

    try:
        if steam_id is not None:
            # Update the main table, setting the steam ID to the new value
            cursor.execute(
                'UPDATE users SET steamid_32 = %s WHERE discord_id = %s',
                (steam_id, discord_id)
            )
        else:
            # Update the main table, setting the steam ID to NULL
            cursor.execute(
                'UPDATE users SET steamid_32 = NULL WHERE discord_id = %s',
                (discord_id,)
            )

    finally:
        connection.commit()
        cursor.close()