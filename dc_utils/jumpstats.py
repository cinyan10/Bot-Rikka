import mysql.connector
from discord import Embed
from config import *
from functions.db_operate.gokz import get_jspb
from functions.steam import convert_steamid
from functions.steam_embed import steam_embed

db_config['database'] = 'gokz'
JUMP_TYPE = ['long jump', 'bunnyhop', 'multi bunnyhop', 'weird jump', 'ladder jump', 'ladderhop', 'jumpbug', 'lowpre bunnyhop', 'lowpre weird jump']
JUMPSTATS = ['Distance', 'IsBlockJump', 'Block', 'Mode', 'JumpType', 'Strafes', 'Sync', 'Pre', 'Max', 'Airtime', 'JumpID', 'Created']


def embed_ljpb(kz_mode, steamid, is_block_jump) -> Embed:
    steamid32 = convert_steamid(steamid, 'steamid32')
    ljpb_data: dict = get_jspb(steamid32, kz_mode, is_block_jump, 0)

    if is_block_jump:
        title = f'LJPB {ljpb_data['Block']} Block Jump'
    else:
        title = f'LJPB {ljpb_data['Distance']}'
    ljpb_embed = steam_embed(
        steamid,
        title=title
    )

    for key in JUMPSTATS:
        ljpb_embed.add_field(name=key, value=ljpb_data[key], inline=True)

    return ljpb_embed


def jumptype_str_to_int(dictionary, search_value):
    for key, value in dictionary.items():
        if value == search_value:
            return key
    return None  # Or raise an exception if you prefer


def fm_distance(distance: int) -> str:
    formatted_distance = distance / 10000  # Convert distance to float with four decimal places
    return f'{formatted_distance:.4f}'


class PlayJumpStats:

    def __init__(self, steamid32, default_mode='kzt', is_cn=True):
        self.steamid32 = steamid32
        self.default_mode = default_mode
        self.is_cn = is_cn

    def js_query(self, count=1, jumptype=0):
        mode = self.default_mode

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        try:
            query = """
            SELECT COUNT(*) + 1 AS rank
            FROM gokz.Localstats
            WHERE Mode = %s AND JumpType = %s AND Distance > (
                SELECT MAX(Distance)
                FROM gokz.LocalStats
                WHERE SteamID32 = %s AND Mode = %s AND JumpType = %s
            )
            """

            cursor.execute(query, (self.steamid32, jumptype, mode, count))
            results = cursor.fetchall()
            return results
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        finally:
            cursor.close()
            connection.close()

    def pb(self, count=1, jumptype=0):
        js_datas = self.js_query(count, jumptype)

        content = ''
        num = 1
        for js_data in js_datas:
            content += f'{num}. {fm_distance(js_data['Distance'])}'
            num += 1
        embed = Embed(title=f'**{JUMP_TYPE[jumptype].upper()} PB**')

        return embed


if __name__ == '__main__':
    ljpb_data: dict = get_jspb(EXA_STEAMID32, 'kzt', False, 0)
    print(ljpb_data)
    pass
