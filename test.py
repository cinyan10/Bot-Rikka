import requests
import json

# Replace YOUR_WEBHOOK_URL with your actual webhook URL
webhook_url = "https://discord.com/api/webhooks/1198569911757308026/p8qXZuo5Rhf7e_5VagkGK8uYaG5Gf9WemfWIh7uBpyv1ySRM34NJJ_ZvmyqqbJgdAyf2"

# Construct the payload for the embedded message
payload = {
    "content": "",
    "embeds": [
        {
            "title": "SERVER LIST",
            "description": "",
            "color": 'blue',  # Hex color code, e.g., red
            "fields": [
                {"name": "AXE GOKZ #1", "value": "MAP 1", "inline": True},
                {"name": "AXE GOKZ #2", "value": "MAP 2", "inline": True},
            ],
            "footer": {"text": "Your Footer"},
        }
    ]
}

# Send the POST request to the webhook URL with the payload
headers = {"Content-Type": "application/json"}
response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)

# Print the response from the server
print(response.text)
