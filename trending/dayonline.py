import mysql.connector
from datetime import datetime, timedelta
from config import db_config, TRENDING_WEBHOOK_URL
import requests
import json


db_config['database'] = 'firstjoin'


def total_player_counting():
    # Establish a connection to the MySQL server
    connection = mysql.connector.connect(**db_config)
    cursor = connection
    try:
        cursor = connection.cursor()

        # Calculate the date one day ago
        one_day_ago_timestamp = datetime.now() - timedelta(days=1)
        # Query to get the total online players count
        total_online_query = (
            "SELECT COUNT(*) AS total_online FROM firstjoin WHERE timestamps >= %s"
        )
        cursor.execute(total_online_query, (one_day_ago_timestamp,))
        total_online_players = cursor.fetchone()[0]

        # Query to get whitelisted players count
        whitelisted_query = (
            "SELECT COUNT(*) AS whitelisted FROM firstjoin WHERE timestamps >= %s AND whitelist = 1"
        )
        cursor.execute(whitelisted_query, (one_day_ago_timestamp,))
        whitelisted_players = cursor.fetchone()[0]

        # Query to get un-whitelisted players count
        un_whitelisted_query = (
            "SELECT COUNT(*) AS un_whitelisted FROM firstjoin WHERE timestamps >= %s AND whitelist = 0"
        )
        cursor.execute(un_whitelisted_query, (one_day_ago_timestamp,))
        un_whitelisted_players = cursor.fetchone()[0]

        return {
            "total_online_players": total_online_players or 0,
            "whitelisted_players": whitelisted_players or 0,
            "un_whitelisted_players": un_whitelisted_players or 0,
        }
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()


def day_online_counting():
    # Establish a connection to the MySQL server
    connection = mysql.connector.connect(**db_config)
    cursor = connection
    try:
        cursor = connection.cursor()

        # Calculate the date one day ago
        one_day_ago_timestamp = int((datetime.now() - timedelta(days=1)).timestamp())
        # Query to get the total online players count
        total_online_query = (
            "SELECT COUNT(*) AS total_online FROM firstjoin WHERE timestamps >= %s"
        )
        cursor.execute(total_online_query, (one_day_ago_timestamp,))
        total_online_players = cursor.fetchone()[0]

        # Query to get whitelisted players count
        whitelisted_query = (
            "SELECT COUNT(*) AS whitelisted FROM firstjoin WHERE timestamps >= %s AND whitelist = 1"
        )
        cursor.execute(whitelisted_query, (one_day_ago_timestamp,))
        whitelisted_players = cursor.fetchone()[0]

        # Query to get un-whitelisted players count
        un_whitelisted_query = (
            "SELECT COUNT(*) AS un_whitelisted FROM firstjoin WHERE timestamps >= %s AND whitelist = 0"
        )
        cursor.execute(un_whitelisted_query, (one_day_ago_timestamp,))
        un_whitelisted_players = cursor.fetchone()[0]

        return {
            "total": total_online_players or 0,
            "whitelisted": whitelisted_players or 0,
            "un_whitelisted": un_whitelisted_players or 0,
        }
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()


def insert_player_counts_to_table(player_counts):
    # Establish a connection to the MySQL server
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    try:
        # Calculate the date for today
        current_date = datetime.now().strftime('%Y-%m-%d')

        # Insert the player counts into the 'online_day' table
        insert_query = (
            "INSERT INTO online_day (date, players_online, whitelisted, un_whitelisted) "
            "VALUES (%s, %s, %s, %s)"
        )
        cursor.execute(insert_query, (current_date, player_counts["total"], player_counts["whitelisted"], player_counts["un_whitelisted"]))

        # Commit the changes to the database
        connection.commit()

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()


def send_discord_webhook(player_counts):
    # Define the embed message payload
    embed_payload = {
        "title": "Yesterday's player count",
        "color": 0x00ff00,  # Green color
        "timestamp": str(datetime.now()),
        "fields": [
            {
                "name": "Total",
                "value": str(player_counts["total"]),
                "inline": True
            },
            {
                "name": "Whitelisted",
                "value": str(player_counts["whitelisted"]),
                "inline": True
            },
            {
                "name": "Un-whitelisted",
                "value": str(player_counts["un_whitelisted"]),
                "inline": True
            }
        ]
    }

    # Create the webhook message payload
    webhook_payload = {
        "embeds": [embed_payload]
    }

    # Send the webhook message to Discord
    response = requests.post(TRENDING_WEBHOOK_URL, data=json.dumps(webhook_payload), headers={"Content-Type": "application/json"})

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        print("Webhook message sent successfully.")
    else:
        print(f"Failed to send webhook message. Status code: {response.status_code}")


if __name__ == "__main__":
    player_counts = day_online_counting()
    print(player_counts)
    # insert_player_counts_to_table(player_counts)
    send_discord_webhook(player_counts)
