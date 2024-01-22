# config.py
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
DB_HOST = os.getenv('DB_HOST')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')


SERVER_LIST_CHANNEL_ID = 1078216816482062367

# Test:
# print(TOKEN, WEBHOOK_URL, DB_PORT, DB_PASSWORD, sep='\n')
