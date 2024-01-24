import asyncio
import discord
from discord.ext import commands
from config import GOKZCN_CHANNEL_ID
from dc_utils.gokzcn import gokzcn_rank
from datetime import datetime

from functions.embed_content import get_jstop


class PaginationView(discord.ui.View):
    def send(self, ctx):
        pass


class Leaderboards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Leaderboards Cog loaded')

    @commands.hybrid_command()
    async def update_gokzcn_rank(self, ctx):
        """update the gokzcn_rank in channel"""
        last_message = None
        try:
            # Get the channel by channel ID
            channel = self.bot.get_channel(GOKZCN_CHANNEL_ID)

            # Check if the channel exists
            if channel is None:
                await ctx.send(f"Channel with ID {GOKZCN_CHANNEL_ID} not found.")
                return

            # Try to fetch the last message in the channel
            async for message in channel.history(limit=1):
                last_message = message

            # Get the content from the gokzcn_rank() function
            content = gokzcn_rank()

            if not last_message:
                # If there are no messages, send a new message
                await channel.send(embed=content)
                await ctx.send(f"New message sent to #{channel.name}.")
            else:
                # If there is an existing message, edit it
                await last_message.edit(embed=content)
                await last_message.edit(content=datetime.now())
                await ctx.send(f"Message edited in #{channel.name}.")

        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")

    @commands.hybrid_command()
    async def test_page(self, ctx):
        # Define the content for each page
        pages = [
            get_jstop(20, 'kzt'),
            get_jstop(20, 'skz'),
            get_jstop(20, 'kzt'),
        ]

        # Initialize the current page index
        current_page = 0

        # Send the initial page
        message = await ctx.send(embed=pages[current_page])

        # Define reaction buttons for navigation
        navigation_buttons = ['⬅️', '➡️']

        # Add reaction buttons to the message
        for button in navigation_buttons:
            await message.add_reaction(button)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in navigation_buttons

        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)

                if str(reaction.emoji) == '➡️':
                    current_page = (current_page + 1) % len(pages)
                elif str(reaction.emoji) == '⬅️':
                    current_page = (current_page - 1) % len(pages)

                await message.edit(embed=pages[current_page])
                await message.remove_reaction(reaction, user)

            except asyncio.TimeoutError:
                break


async def setup(bot: commands):
    await bot.add_cog(Leaderboards(bot))
