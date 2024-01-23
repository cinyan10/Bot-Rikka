import asyncio
from datetime import datetime, timezone

import discord

from functions.embed_content import get_jstop
from functions.query import query_all_servers, query_server_embed


async def server_list_embed_loop(message):
    while True:
        # Function that updates the content of the embedded message
        current_datetime = datetime.now(timezone.utc)
        new_content = query_all_servers()
        embed = discord.Embed(
            title='AXE SERVER LIST',
            description=new_content,
            colour=0x60FFFF,
            timestamp=current_datetime
        )

        # Edit the embedded message with the new content
        await message.edit(embed=embed)

        # Wait for one minute before the next update
        await asyncio.sleep(60)


async def gz_server_embeds_loop(message: discord.Message, servers):
    while True:
        embeds = [query_server_embed(s) for s in servers]
        await message.edit(embeds=embeds)
        await asyncio.sleep(60)


async def bj_server_embeds_loop(message: discord.Message, servers):
    while True:
        embeds = [query_server_embed(s) for s in servers]
        await message.edit(embeds=embeds)
        await asyncio.sleep(60)


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
        await asyncio.sleep(60)
