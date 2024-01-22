from pymysql import Connection
from config import DB_HOST, DB_PORT, DB_PASSWORD, DB_USER
import mysql.connector

# About Database Functions
connection = Connection(
    host=DB_HOST,
    port=int(DB_PORT),
    user=DB_USER,
    password=DB_PASSWORD,
)

KZ_MODES = {'kzt': 2, 'skz': 1, 'vnl': 0}

db_config = {
        'user': DB_USER,
        'password': DB_PASSWORD,
        'host': DB_HOST,
        'database': 'gokz',
        'raise_on_warnings': True,
        'port': DB_PORT,
    }

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


def retrieve_user_name(steamid_32):
    cursor = connection.cursor()
    connection.select_db('firstjoin')
    cursor.execute(
        'SELECT name FROM firstjoin WHERE auth = %s',
        (steamid_32,)
    )
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None


def query_jumpstats_top(limit: int = 10, mode: str = 'kzt') -> str:
    # Establish a database connection
    conn = mysql.connector.connect(**db_config)

    # Prepare the SQL query
    query = f'''
    SELECT j.SteamID32, j.Distance
    FROM Jumpstats j
    JOIN Players p ON j.SteamID32 = p.SteamID32
    WHERE j.JumpType = 0 AND j.Mode = {KZ_MODES[mode]} AND p.Cheater != 1
    ORDER BY j.Distance DESC
    LIMIT {limit}
    '''

    # Execute the query
    cursor = conn.cursor()
    cursor.execute(query)

    # Fetch the results
    rows = cursor.fetchall()

    # Print the results
    result = ''
    for steam_id, distance in rows:
        result += f'SteamID32: {steam_id}, Distance: {distance}\n'

    # Close the cursor and connection
    cursor.close()
    conn.close()
    return result

