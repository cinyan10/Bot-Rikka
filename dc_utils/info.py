import mysql.connector
from config import db_config


def set_bili(ctx, discord_id, bili_uid) -> str:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    try:
        update_query = "UPDATE discord.users SET bili_uid = %s WHERE discord_id = %s"

        cursor.execute(update_query, (bili_uid, discord_id))

        conn.commit()

        if cursor.rowcount > 0:
            return f"Bili_uid updated for Discord user {discord_id}"
        else:
            return f"Discord user {discord_id} not found in the database. Please /bind_steam first"

    except mysql.connector.Error as err:
        return f"Error: {err}"
    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()
