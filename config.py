# config.py
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_PORT = os.getenv('MYSQL_PORT')

# Test:
# print(TOKEN, WEBHOOK_URL, MYSQL_PORT, MYSQL_PASSWORD, sep='\n')
