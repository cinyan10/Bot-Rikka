from datetime import timedelta
from functions.steam import *
from pymysql import Connection
from config import DB_HOST, DB_PORT, DB_PASSWORD, DB_USER
import mysql.connector
from functions.kreedz import *


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


def discordid_to_steamid(discord_id):
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


def get_steam_user_name(steamid_32):
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
    SELECT j.SteamID32, MAX(j.Distance) as MaxDistance
    FROM Jumpstats j
    JOIN Players p ON j.SteamID32 = p.SteamID32
    WHERE j.JumpType = 0 AND j.Mode = {KZ_MODES[mode]} AND p.Cheater != 1
    GROUP BY j.SteamID32
    ORDER BY MaxDistance DESC
    LIMIT {limit}
    '''

    # Execute the query
    cursor = conn.cursor()
    cursor.execute(query)

    # Fetch the results
    rows = cursor.fetchall()

    # Process the results
    result = ''
    rank = 1
    for steamid32, distance in rows:
        steamid = steamid32_to_steamid(str(steamid32))
        kzgoeu_url = get_kzgoeu_profile_url(steamid, mode)
        name = get_steam_user_name(steamid)
        formatted_distance = distance / 10000  # Convert distance to float with four decimal places
        result += f'[{rank}. {name}]({kzgoeu_url}) - {formatted_distance:.4f}\n'
        rank += 1

    # Close the cursor and connection
    cursor.close()
    conn.close()
    return result


def get_total_playtime(steamid32):
    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Prepare the SQL query to sum all runtimes for a given SteamID32
    query = '''
    SELECT SUM(Runtime)
    FROM Times
    WHERE SteamID32 = %s
    '''

    # Execute the query
    cursor.execute(query, (steamid32,))

    # Fetch the result
    result = cursor.fetchone()
    total_runtime_milliseconds = int(result[0]) if result[0] is not None else 0

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # Convert the total runtime from milliseconds to a timedelta object
    total_runtime = timedelta(milliseconds=total_runtime_milliseconds)

    # Format the timedelta to a string in the format of hours:minutes:seconds
    # Note: This will only show the hours contained in one day if you have more than 24 hours of playtime
    # For showing total hours exceeding 24, you can calculate it by (total_runtime.days * 24 + total_runtime.seconds // 3600)
    total_hours = total_runtime.days * 24 + total_runtime.seconds // 3600
    total_minutes = (total_runtime.seconds // 60) % 60
    total_seconds = total_runtime.seconds % 60
    playtime_str = f"{total_hours} hours, {total_minutes} minutes, {total_seconds} seconds"

    return playtime_str


if __name__ == "__main__":
    rs = query_jumpstats_top(20)
    print(rs)
