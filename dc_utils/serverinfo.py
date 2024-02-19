import asyncio
import discord

from dc_utils.server_status import embeds_server_status
from functions.embed_content import get_jstop
from functions.steam.a2s import query_all_servers, query_server_embed


async def server_list_embed_loop(message):
    while True:
        await message.edit(embed=query_all_servers())
        await asyncio.sleep(20)


async def gz_server_embeds_loop(message: discord.Message, servers, bot):
    while True:
        embeds = [await query_server_embed(s, bot) for s in servers]
        await message.edit(embeds=embeds)
        await asyncio.sleep(59)


async def bj_server_embeds_loop(message: discord.Message, servers, bot):
    while True:
        embeds = [await query_server_embed(s, bot) for s in servers]
        await message.edit(embeds=embeds)
        await asyncio.sleep(60)


async def server_status_loop(message: discord.Message):
    while True:
        embeds = embeds_server_status()
        await message.edit(embeds=embeds)
        await asyncio.sleep(61)


async def jstop_embeds_loop(message: discord.Message):
    while True:
        embeds = []
        embed1 = get_jstop(20, 'kzt')
        embed2 = get_jstop(10, 'skz')
        embed3 = get_jstop(10, 'vnl')
        embeds.append(embed1)
        embeds.append(embed2)
        embeds.append(embed3)
        await message.edit(embeds=embeds)
        await asyncio.sleep(10800)
