import mysql.connector
from config import *

db_config['database'] = 'gokz'

def get_ljpb(steamid32, kz_mode, is_block_jump, jump_type) -> dict:
    connection = None
    cursor = None

    try:
        # Connect to the database using the imported db_config
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Define the SQL query to retrieve the best jump data
        query = """
        SELECT *
        FROM gokz.Jumpstats
        WHERE SteamID32 = %s
        AND Mode = %s
        AND (IsBlockJump = %s OR %s = 0)
        AND JumpType = %s
        ORDER BY Distance DESC
        LIMIT 1
        """

        # Set is_block_jump to 1 if it is True, otherwise set it to 0
        is_block_jump_value = 1 if is_block_jump else 0
        mode = KZ_MODES.index(kz_mode)
        # Execute the SQL query with the provided parameters
        cursor.execute(query, (steamid32, mode, is_block_jump_value, is_block_jump_value, jump_type))

        # Fetch the result
        result = cursor.fetchone()

        if result:
            # format
            result['Pre'] = result['Pre'] / 100.0
            result['Max'] = result['Max'] / 100.0
            result['Sync'] = result['Sync'] / 100.0
            result['Distance'] = result['Distance'] / 10000.0
            result['JumpType'] = JUMP_TYPE[result['JumpType']]
            result['Airtime'] = result['Airtime'] / 10000.0
            result['Mode'] = KZ_MODES[result['Mode']].upper()
            return result  # Returns the full jump data as a dictionary
        else:
            print('No valid data')
            return {}

    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return {}

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


import mysql.connector
from config import db_config  # Import the db_config module

# Function to query player's best distances grouped by JumpType
def get_jspb(steamid32, mode):
    mode = KZ_MODES.index(mode)
    try:
        # Establish a connection to your MySQL database using imported config values
        conn = mysql.connector.connect(**db_config)

        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        # Execute a SELECT query to retrieve best distances grouped by JumpType
        cursor.execute("""
            SELECT JumpType, MAX(Distance)
            FROM gokz.Jumpstats
            WHERE SteamID32 = %s AND Mode = %s
            GROUP BY JumpType
        """, (steamid32, mode))

        # Fetch all the results (best distances for each jump type)
        results = cursor.fetchall()

        # Create a dictionary to store the results with jump types as keys
        best_distances_by_jumptype = {jump_type: best_distance for jump_type, best_distance in results}

        return best_distances_by_jumptype

    except mysql.connector.Error as e:
        print(f"MySQL error: {e}")
        return None

    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    # Example usage:
    steam_id32_to_query = STEAMID32  # Replace with the SteamID32 you want to query
    mode_to_query = 'kzt'  # Replace with the desired mode
    jspb = get_jspb(steam_id32_to_query, mode_to_query)
    print(type(jspb))
    for k, v in jspb.items():
        print(k, v)
