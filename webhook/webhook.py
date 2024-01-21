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
            "color": 0x60FFFF,  # Hex color code, e.g., red
            "fields": [
                {"name": "AXE GOKZ 广州#1", "value": "kz_lionheart T6\n一只波奇酱♪ 小尐 吕墨菲", "inline": False},
                {"name": "AXE GOKZ 广州#2", "value": "kz_lionheart T6\n路小雨", "inline": False},
                {"name": "AXE GOKZ 广州#3", "value": "kz_lionheart T6\n别打我 我是热狗", "inline": False},
                {"name": "AXE GOKZ 广州#4", "value": "kz_lionheart T6\nHarutya", "inline": False},
                {"name": "AXE GOKZ 广州#5", "value": "kz_lionheart T6\n", "inline": False},
                {"name": "AXE GOKZ 广州#6", "value": "kz_lionheart T6\n树叶飘零 GoneHway", "inline": False},
                {"name": "AXE GOKZ 北京#1", "value": "kz_lionheart T6\n", "inline": False},
                {"name": "AXE GOKZ 北京#2", "value": "kz_lionheart T6\n尘缘隐匿于星海 Tikeone 潜在鸣猩哥 17号", "inline": False},
                {"name": "AXE GOKZ 北京#3", "value": "kz_lionheart T6\n", "inline": False},
                {"name": "AXE GOKZ 北京#4", "value": "kz_lionheart T6\n", "inline": False},
                {"name": "AXE GOKZ 北京#5", "value": "kz_lionheart T6\n", "inline": False},
                {"name": "AXE GOKZ 北京#6", "value": "kz_lionheart T6\n", "inline": False},
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
