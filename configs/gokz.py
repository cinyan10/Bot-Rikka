import json

JUMP_TYPE = ['long jump', 'bunnyhop', 'multi bunnyhop', 'weird jump',
             'ladder jump', 'ladderhop', 'jumpbug', 'lowpre bunnyhop', 'lowpre weird jump']
JUMPSTATS = ['Distance', 'IsBlockJump', 'Block', 'Mode', 'JumpType',
             'Strafes', 'Sync', 'Pre', 'Max', 'Airtime', 'JumpID', 'Created']
KZ_MODES = ['vnl', 'skz', 'kzt']


with open('./maps_tier.json', 'r', encoding='utf-8') as f:
    MAP_TIERS = json.load(f)
    pass

GLOBAL_API_URL = "https://kztimerglobal.com/"
KZGOEU_MAPS_URL = 'https://kzgo.eu/maps/'
MAP_IMAGE_URL = "https://raw.githubusercontent.com/KZGlobalTeam/map-images/master/images/"
