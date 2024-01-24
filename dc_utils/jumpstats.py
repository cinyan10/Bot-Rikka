from discord import Embed
from config import *
from functions.db_operate.gokz import get_ljpb, get_jspb
from functions.steam import convert_steamid
from functions.steam_embed import steam_embed


def embed_ljpb(kz_mode, steamid, is_block_jump) -> Embed:
    steamid32 = convert_steamid(steamid, 'steamid32')
    ljpb_data: dict = get_ljpb(steamid32, kz_mode, is_block_jump, 0)

    if is_block_jump:
        title = f'LJPB: {ljpb_data['Block']} Block Jump'
    else:
        title = f'LJPB: {ljpb_data['Distance']}'
    ljpb_embed = steam_embed(
        steamid,
        title=title
    )

    for key in JUMPSTATS:
        ljpb_embed.add_field(name=key, value=ljpb_data[key], inline=True)

    return ljpb_embed


def embed_jspb(kz_mode, steamid) -> Embed:
    steamid32 = convert_steamid(steamid, 'steamid32')
    jspb_data: dict = get_jspb(steamid32, kz_mode)

    title = f'Jump Stats: {jspb_data['Mode']}'
    jspb_embed = steam_embed(
        steamid,
        title=title
    )

    return jspb_embed


if __name__ == '__main__':
    pass
