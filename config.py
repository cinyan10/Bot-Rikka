import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

NEZHA_TOKEN = os.getenv('NEZHA_TOKEN')

PROJECT_DIR = os.path.dirname(__file__)
