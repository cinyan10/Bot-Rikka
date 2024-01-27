import mysql.connector
from config import *


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
    pass
