import mysql.connector
from config import *


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


def get_jspb(kz_mode, steamid) -> dict:
    pass

if __name__ == "__main__":
    # Example usage (assuming db_config is imported from your config module):
    steamid32 = EXA_STEAMID32  # Replace with the desired SteamID32
    kz_mode = "kzt"  # Replace with the desired kz_mode
    is_block_jump = False  # Set to True or False as needed
    jump_type = 0  # Replace with the desired JumpType
    best_jump_data = get_ljpb(steamid32, kz_mode, is_block_jump, jump_type)

    if best_jump_data:
        print("Player's Best Jump Data:")
        print(type(best_jump_data))
        for key, value in best_jump_data.items():
            print(f"{key}: {value}")

    else:
        print("No data found for the specified criteria.")
