import mysql.connector
from config import *


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


if __name__ == "__main__":
    partial_name = "Exa"
    auth_values = find_player_by_name_partial_match(partial_name)
    if auth_values:
        print("Found matching players with 'auth' values:", auth_values)
    else:
        print("No matching players found or more than 5 matching players.")
