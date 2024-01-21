import requests
import json
from valve.source import a2s
from servers import *
from query import query_server_simple


# Replace YOUR_WEBHOOK_URL with your actual webhook URL
webhook_url = "https://discord.com/api/webhooks/1198569911757308026/p8qXZuo5Rhf7e_5VagkGK8uYaG5Gf9WemfWIh7uBpyv1ySRM34NJJ_ZvmyqqbJgdAyf2"


# ip="43.139.56.16", port=10001
# Construct the payload for the embedded message
def query_servers():
    rs = ''
    for s in servers:
        rs += query_server_simple(s)


content = ''
for s in servers:
    content += query_server_simple(s)

payload = {
    "content": "",
    "embeds": [
        {
            "title": "SERVER LIST",
            "description": content,
            "color": 0x60FFFF,  # Hex color code, e.g., red
            "footer": {"text": "Your Footer"},
        }
    ]
}

# Send the POST request to the webhook URL with the payload
headers = {"Content-Type": "application/json"}
response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)

# Print the response from the server
print(response.text)
