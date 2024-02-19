import requests
import json
from configs.servers import SERVER_LIST
from configs.discord import WEBHOOK_URL
from functions.steam.a2s import query_single_server


def send_webhook():
    info_data = ''
    for s in SERVER_LIST:
        info_data += query_single_server(s)

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
    response = requests.post(WEBHOOK_URL, data=json.dumps(payload), headers=headers)

    # Print the response from the server
    print(response.text)


if __name__ == "__main__":
    pass
