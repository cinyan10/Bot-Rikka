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

    if steam_id is not None:
        # Update the temporary table with the new steam ID
        cursor.execute('UPDATE temp_users SET steamid_32 = %s', (steam_id,))
    else:
        # Update the temporary table to set steam ID to NULL
        cursor.execute('UPDATE temp_users SET steamid_32 = NULL')

        # Update the main table based on the temporary table
    cursor.execute(
        'UPDATE users INNER JOIN temp_users ON users.steamid = temp_users.steamid SET users.steamid = temp_users.steamid')

    # Drop the temporary table
    cursor.execute('DROP TEMPORARY TABLE IF EXISTS temp_users')

    connection.commit()
    cursor.close()