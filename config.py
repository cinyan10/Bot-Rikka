# config.py
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

# DATABASE
DB_HOST = os.getenv('DB_HOST')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')

db_config = {
            'user': DB_USER,
            'password': DB_PASSWORD,
            'host': DB_HOST,
            'port': DB_PORT
        }

GUILD_ID = 1042847878894321824

# CHANNEL_ID
SERVER_LIST_CHANNEL_ID = 1078216816482062367
GUANGZHOU_CHANNEL_ID = 1198958601058910329
BEIJING_CHANNEL_ID = 1198958645698904064
TEST_CHANNEL_ID = 1192695338616762398
PRINT_CHANNEL_ID = 1199047537500356750
GOKZCN_CHANNEL_ID = 1199000862673096804
JSTOP_CLIENT_ID = 1199000627859173457


# STEAM
STEAM_API_KEY = os.getenv('STEAM_API_KEY')
GROUP_ID = '43691138'
GROUP_URL = "https://steamcommunity.com/groups/axekz/memberslistxml/?xml=1"

# GOKZ
JUMP_TYPE = ['long jump', 'bunnyhop', 'multi bunnyhop', 'weird jump', 'ladder jump', 'ladderhop', 'jumpbug', 'lowpre bunnyhop', 'lowpre weird jump']
JUMPSTATS = ['Distance', 'IsBlockJump', 'Block', 'Mode', 'JumpType', 'Strafes', 'Sync', 'Pre', 'Max', 'Airtime', 'JumpID', 'Created']
KZ_MODES = ['vnl', 'skz', 'kzt']

# SOME CONFIG FOR TESTING
STEAMID = "STEAM_1:0:530988200"
STEAMID32 = '1061976400'
STEAMID64 = "76561199022242128"
DISCORD_ID = '434525118425726977'
