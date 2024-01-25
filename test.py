from functions.database import get_playtime
from functions.db_operate.firstjoin import get_whitelisted_players
from functions.steam import convert_steamid
from config import db_config
import mysql.connector


def update_total(steamid, total):
    # Establish a MySQL database connection using your db_config
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Retrieve the name and timestamps (last_accountuse) from firstjoin.firstjoin based on the auth (steamid)
    cursor.execute("SELECT name, timestamps FROM firstjoin WHERE auth = %s", (steamid,))
    player_data = cursor.fetchone()

    if player_data:
        playername, last_accountuse = player_data
        # Check if the steamid already exists in the mostactive table
        cursor.execute("SELECT * FROM mostactive WHERE steamid = %s", (steamid,))
        existing_data = cursor.fetchone()

        if existing_data:
            # If the steamid exists in mostactive, update the values
            cursor.execute("UPDATE mostactive SET playername = %s, last_accountuse = %s, total = %s WHERE steamid = %s",
                           (playername, last_accountuse, total, steamid))
        else:
            # If the steamid doesn't exist in mostactive, insert the data
            cursor.execute("INSERT INTO mostactive (playername, last_accountuse, steamid, total) VALUES (%s, %s, %s, %s)",
                           (playername, last_accountuse, steamid, total))

        # Commit changes and close the database connection
        conn.commit()
        conn.close()
    else:
        # If the steamid doesn't exist in firstjoin.firstjoin, handle the case as needed (e.g., raise an error or log a message)
        conn.close()
        raise Exception(f"SteamID {steamid} not found in firstjoin.firstjoin table")


steamids = get_whitelisted_players()
count = 0
for steamid in steamids:
    count = count + 1
    print(f"{count}/{len(steamids)} {steamid}")
    steamid32 = convert_steamid(steamid, "steamid32")
    total = get_playtime(steamid32)
    seconds = total[0] * 3600 + total[1] * 60 + total[2]
    update_total(steamid, seconds)
