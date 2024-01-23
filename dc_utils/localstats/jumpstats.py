import mysql.connector
from discord import Embed
from config import *

db_config['database'] = 'gokz'
JUMP_TYPE = ['long jump', 'bunnyhop', 'multi bunnyhop', 'weird jump', 'ladder jump', 'ladderhop', 'jumpbug', 'lowpre bunnyhop', 'lowpre weird jump']


def jumptype_str_to_int(dictionary, search_value):
    for key, value in dictionary.items():
        if value == search_value:
            return key
    return None  # Or raise an exception if you prefer


def fm_distance(distance: int) -> str:
    formatted_distance = distance / 10000  # Convert distance to float with four decimal places
    return f'{formatted_distance:.4f}'


def get_player_rank_by_distance(steamid32, mode, jumptype):
    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        query = """
        SELECT COUNT(*) + 1 AS rank
        FROM gokz.Jumpstats
        WHERE Mode = %s AND JumpType = %s AND Distance > (
            SELECT Distance
            FROM gokz.Jumpstats
            WHERE SteamID32 = %s AND Mode = %s AND JumpType = %s
        )
        """
        cursor.execute(query, (mode, jumptype, steamid32, mode, jumptype))
        result = cursor.fetchone()
        return result[0] if result else None

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


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
            FROM gokz.Jumpstats
            WHERE Mode = %s AND JumpType = %s AND Distance > (
                SELECT MAX(Distance)
                FROM gokz.Jumpstats
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
    rank = get_player_rank_by_distance(EXA_STEAMID32, 'kzt', 0)
    print(f"The player's rank is: {rank}")
