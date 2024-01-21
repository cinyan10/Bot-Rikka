import os
import requests
import json
from dotenv import load_dotenv
from servers import *
from query import query_server_simple


def send_webhook():
    # Replace YOUR_WEBHOOK_URL with your actual webhook URL
    load_dotenv()
    webhook_url = os.getenv('WEBHOOK_URL')
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