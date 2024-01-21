import os
import requests
import json
from dotenv import load_dotenv
from servers import *
from query import query_server_simple


def send_webhook():
    # Replace YOUR_WEBHOOK_URL with your actual webhook URL
    webhook_url = 'https://discord.com/api/webhooks/1198613157225177170/M8R3R3X8VSgupBG9Iup3xFj6aDtUopeYUbeMDUlxKh2y8aEQJdUV6b21PqLEA7OSJ47n'
    info_data = ''
    for s in servers:
        info_data += query_server_simple(s)

    payload = {
        "content": "",
        "embeds": [
            {
                "title": "SERVER LIST",
                "description": info_data,
                "color": 0x60FFFF,  # Hex color code, e.g., red
                # "footer": {"text": "Your Footer"},
            }
        ]
    }

    # Send the POST request to the webhook URL with the payload
    headers = {"Content-Type": "application/json"}
    response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)

    # Print the response from the server
    print(response.text)


if __name__ == "__main__":
    pass