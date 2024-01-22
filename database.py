from pymysql import Connection, MySQLError
from config import DB_PASSWORD, DB_USER, DB_PORT, DB_HOST
import logging


def get_database_connection():
    return Connection(
        host=DB_HOST,
        port=int(DB_PORT),
        user=DB_USER,
        password=DB_PASSWORD,
    )


def retrieve_steam_id(discord_id):
    connection = None
    try:
        connection = get_database_connection()
        with connection.cursor() as cursor:
            connection.select_db('discord')
            cursor.execute(
                'SELECT steamid_32 FROM users WHERE discord_id = %s',
                (discord_id,)
            )
            result = cursor.fetchone()
            return result[0] if result else None
    except MySQLError as e:
        # Handle the exception (log it, raise it, etc.)
        print(f'Error: {e}')
        logging.error(f"Error in retrieve_steam_id: {e}")
        pass
    finally:
        if connection:
            connection.close()


def retrieve_join_date(steam_id):
    connection = None
    try:
        connection = get_database_connection()
        with connection.cursor() as cursor:
            connection.select_db('firstjoin')
            cursor.execute(
                'SELECT joindate FROM firstjoin WHERE auth = %s',
                (steam_id,)
            )
            result = cursor.fetchone()
            return result[0] if result else None
    except MySQLError as e:
        print(f'Error: {e}')
        logging.error(f"Error in retrieve_steam_id: {e}")
        pass
    finally:
        if connection:
            connection.close()


# Function to retrieve last_seen from firstjoin table by steamid
def retrieve_last_seen(steam_id):
    connection = None
    try:
        connection = get_database_connection()
        with connection.cursor() as cursor:
            connection.select_db('firstjoin')
            cursor.execute(
                'SELECT lastseen FROM firstjoin WHERE auth = %s',
                (steam_id,)
            )
            result = cursor.fetchone()
            return result[0] if result else None
    except MySQLError as e:
        print(f'Error: {e}')
        logging.error(f"Error in retrieve_steam_id: {e}")
        pass
    finally:
        if connection:
            connection.close()


def reset_user_steam(discord_id, steam_id):
    connection = None
    try:
        connection = get_database_connection()
        with connection.cursor() as cursor:
            connection.select_db('discord')
            if steam_id is not None:
                cursor.execute(
                    'UPDATE users SET steamid_32 = %s WHERE discord_id = %s',
                    (steam_id, discord_id)
                )
            else:
                cursor.execute(
                    'UPDATE users SET steamid_32 = NULL WHERE discord_id = %s',
                    (discord_id,)
                )
        connection.commit()
    except MySQLError as e:
        print(f'Error: {e}')
        logging.error(f"Error in retrieve_steam_id: {e}")
        pass
    finally:
        if connection:
            connection.close()


def retrieve_user_name(steamid_32):
    connection = None
    try:
        connection = get_database_connection()
        with connection.cursor() as cursor:
            connection.select_db('firstjoin')
            cursor.execute(
                'SELECT name FROM firstjoin WHERE auth = %s',
                (steamid_32,)
            )
            result = cursor.fetchone()
            return result[0] if result else None
    except MySQLError as e:
        print(f'Error: {e}')
        logging.error(f"Error in retrieve_steam_id: {e}")
        pass
    finally:
        if connection:
            connection.close()
