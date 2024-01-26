import asyncio
from datetime import datetime

import discord
from discord import Embed
from discord.ext import commands
from config import *
from dc_utils.server_status import get_server_status, embeds_server_status
from dc_utils.serverinfo import server_list_embed_loop, gz_server_embeds_loop, bj_server_embeds_loop, jstop_embeds_loop
from functions.misc import get_or_create_message
from functions.servers import SERVER_LIST


class LoopUpdates(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('LoopUpdates loaded')

        server_list_channel = self.bot.get_channel(SERVER_LIST_CHANNEL_ID)
        guangzhou_channel = self.bot.get_channel(GUANGZHOU_CHANNEL_ID)
        beijing_channel = self.bot.get_channel(BEIJING_CHANNEL_ID)
        jstop_channel = self.bot.get_channel(JSTOP_CLIENT_ID)

        # Check if a message already exists in the channel
        existing_message = await get_or_create_message(server_list_channel, 'AXE SERVER LIST', 'Loading...')
        existing_message_2 = await get_or_create_message(guangzhou_channel, '广州 SERVER LIST', 'Loading...')
        existing_message_3 = await get_or_create_message(beijing_channel, '北京 SERVER LIST', 'Loading...')
        existing_message_4 = await get_or_create_message(jstop_channel, 'LocalStats Top', 'Loading...')

        # Start the dynamic embed loop
        loop_task_1 = asyncio.create_task(server_list_embed_loop(existing_message))
        loop_task_2 = asyncio.create_task(gz_server_embeds_loop(existing_message_2, SERVER_LIST[:6]))
        loop_task_3 = asyncio.create_task(bj_server_embeds_loop(existing_message_3, SERVER_LIST[6:]))
        loop_task_4 = asyncio.create_task(jstop_embeds_loop(existing_message_4))

        # Wait for all loop tasks to complete
        await loop_task_1
        await loop_task_2
        await loop_task_3
        await loop_task_4

    @commands.hybrid_command()
    async def server_status(self, ctx):
        channel = self.bot.get_channel(STATUS_CHANNEL_ID)
        embeds = embeds_server_status()
        await channel.send(embed=embeds)
        await ctx.send(embed=Embed(title='Server Status Send'))


async def setup(bot):
    await bot.add_cog(LoopUpdates(bot))
