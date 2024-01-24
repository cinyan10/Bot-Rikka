import mysql.connector
from config import * # Import the db_config module


# Function to query kz_mode by discord_id
def get_kz_mode(discord_id):

    cursor = None
    conn = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT kz_mode FROM discord.users WHERE discord_id = %s", (discord_id,))

        result = cursor.fetchone()

        if result:
            return result[0]  # Return the kz_mode value
        else:
            return None  # User not found or no kz_mode information

    except mysql.connector.Error as e:
        print(f"MySQL error: {e}")
        return None

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    # Example usage:
    discord_id_to_query = DISCORDID
    kz_mode = get_kz_mode(discord_id_to_query)

    if kz_mode is not None:
        print(f"kz_mode for user {discord_id_to_query}: {kz_mode}")
    else:
        print(f"User {discord_id_to_query} not found or no kz_mode information.")
