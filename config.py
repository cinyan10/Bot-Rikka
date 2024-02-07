import json
import os
from dotenv import load_dotenv

from functions.server import Server

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
TRENDING_WEBHOOK_URL = os.getenv('TRENDING_WEBHOOK_URL')
NEZHA_TOKEN = os.getenv('NEZHA_TOKEN')

# DATABASE
DB_HOST = os.getenv('DB_HOST')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')

GLOBAL_API_URL = "https://kztimerglobal.com/"

KZGOEU_MAPS_URL = 'https://kzgo.eu/maps/'
MAP_IMAGE_URL = "https://raw.githubusercontent.com/KZGlobalTeam/map-images/master/images/"

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
PLAYTIME_CHANNEL_ID = 1200131709958627479
STATUS_CHANNEL_ID = 1200415697948397610
INFO_CHANNEL_ID = 1073318661084946442
WELCOME_CHANNEL_ID = 1198602950357041183

# ANNOUNCEMENT

ANNOUNCEMENT_MESSAGE_ID = 1201481306685587477

GUILD_LINK = 'https://discord.gg/GyKks7YNCn'

# ROLE ID
WL_ROLE_ID = 1200728830042714132

# STEAM
STEAM_API_KEY = os.getenv('STEAM_API_KEY')
GROUP_ID = '44318306'
GROUP_URL = "https://steamcommunity.com/groups/axekz/memberslistxml/?xml=1"

# GOKZ
JUMP_TYPE = ['long jump', 'bunnyhop', 'multi bunnyhop', 'weird jump',
             'ladder jump', 'ladderhop', 'jumpbug', 'lowpre bunnyhop', 'lowpre weird jump']
JUMPSTATS = ['Distance', 'IsBlockJump', 'Block', 'Mode', 'JumpType',
             'Strafes', 'Sync', 'Pre', 'Max', 'Airtime', 'JumpID', 'Created']
KZ_MODES = ['vnl', 'skz', 'kzt']

# SOME CONFIG FOR TESTING
STEAMID = "STEAM_1:0:530988200"
STEAMID32 = '1061976400'
STEAMID64 = "76561199022242128"
DISCORD_ID = '434525118425726977'

with open('resource/maps_tier.json', 'r', encoding='utf-8') as f:
    MAP_TIERS = json.load(f)

SERVER_LIST = [
    Server('GOKZ GuangZhou #1', 'GOKZ 广州#1', '广州1', 1, '43.139.56.16', 10001, 1200514677495570544),
    Server('GOKZ GuangZhou #2', 'GOKZ 广州#2', '广州2', 2, '43.139.56.16', 10002, 1200514715697287178),
    Server('GOKZ GuangZhou #3', 'GOKZ 广州#3', '广州3', 3, '43.139.56.16', 10003, 1200514743773954058),
    Server('GOKZ GuangZhou #4', 'GOKZ 广州#4', '广州4', 4, '43.139.56.16', 10004, 1200514782751641781),
    Server('GOKZ GuangZhou #5', 'GOKZ 广州#5', '广州5', 5, '43.139.56.16', 10005, 1200514805237301280),
    Server('GOKZ GuangZhou #6', 'GOKZ 广州#6', '广州6', 6, '43.139.56.16', 10006, 1200514845506818220),
    Server('GOKZ BeiJing #1', 'GOKZ 北京#1', '北京1', 7, '43.138.126.94', 10001, 1200514868629999756),
    Server('GOKZ BeiJing #2', 'GOKZ 北京#2', '北京2', 8, '43.138.126.94', 10002, 1200514889437941930),
    Server('GOKZ BeiJing #3', 'GOKZ 北京#3', '北京3', 9, '43.138.126.94', 10003, 1200514912703754360),
    Server('GOKZ BeiJing #4', 'GOKZ 北京#4', '北京4', 10, '43.138.126.94', 10004, 1200514930315640905),
    Server('GOKZ BeiJing #5', 'GOKZ 北京#5', '北京5', 11, '43.138.126.94', 10005, 1200514949554913342),
    Server('GOKZ BeiJing #6', 'GOKZ 北京#6', '北京6', 12, '43.138.126.94', 10006, 1200514970543198318),
]
