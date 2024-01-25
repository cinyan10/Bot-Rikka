import mysql.connector
from config import *
from functions.steam import convert_steamid, is_user_in_steam_group

db_config['database'] = "firstjoin"


def find_player_by_name_partial_match(name):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    query = f"SELECT auth FROM firstjoin.firstjoin WHERE name LIKE '%{name}%'"
    cursor.execute(query)

    results = cursor.fetchall()

    conn.close()

    if len(results) < 5:
        return [row[0] for row in results]  # Extract and return the 'auth' values
    else:
        return []  # Return an empty list if there are more than or equal to 5 results


def update_whitelist_status(steamid):
    conn = mysql.connector.connect(**db_config)
    try:
        steamid64 = convert_steamid(steamid, 'steamid64')
        is_in_group = is_user_in_steam_group(str(steamid64))
        # Update the whitelist status in the database
        cursor = conn.cursor()
        cursor.execute("UPDATE firstjoin SET whitelist = %s WHERE auth = %s", (is_in_group, steamid))
        conn.commit()
        cursor.close()
        return True

    except mysql.connector.Error as e:
        print(f"MySQL error: {e}")
        return False

    except Exception as e:
        print(f"Error updating whitelist status: {e}")
        return False

    finally:
        conn.close()


def update_whitelist_for_users() -> None:
    conn = mysql.connector.connect(**db_config)
    try:
        cursor = conn.cursor()

        # Select users with whitelist = 0
        cursor.execute("SELECT auth FROM firstjoin.firstjoin WHERE whitelist = 0")
        users_to_update = cursor.fetchall()

        amount = len(users_to_update)
        count = 0

        for user in users_to_update:
            count += 1
            steamid = user[0]

            # Convert SteamID to SteamID64
            steamid64 = convert_steamid(steamid, 'steamid64')

            # Check if the user is in the specified group
            is_in_group = is_user_in_steam_group(str(steamid64))
            print(f"Updating whitelist for user {user[0]}, {count} / {amount}")

            # Update whitelist status (1 for whitelisted, 0 for not whitelisted)
            cursor.execute("UPDATE firstjoin.firstjoin SET whitelist = %s WHERE auth = %s", (int(is_in_group), steamid))

        # Commit changes
        conn.commit()
        cursor.close()

    except mysql.connector.Error as e:
        print(f"MySQL error: {e}")

    except Exception as e:
        print(f"Error updating whitelist status: {e}")

    finally:
        conn.close()


def get_whitelisted_players() -> list:
    """return a list of steamID"""
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**db_config)
        if not conn.is_connected():
            print("Database connection failed.")
            return []
        cursor = conn.cursor()
        # Execute SQL query to retrieve Steam IDs with whitelist = 1
        cursor.execute("SELECT auth FROM firstjoin.firstjoin WHERE whitelist = 1")

        whitelisted_players = cursor.fetchall()

        # Extract Steam IDs from the result and store them in a list
        steam_ids = [row[0] for row in whitelisted_players]
        return steam_ids
    except mysql.connector.Error as e:
        print(f"MySQL error: {e}")
        return []
    except Exception as e:
        print(f"Error fetching whitelisted players: {e}")
        return []
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if conn.is_connected():
            conn.close()
            print("Database connection closed")


if __name__ == "__main__":
    players = get_whitelisted_players()
    print(players)
