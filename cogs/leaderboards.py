from discord.ext import commands
from config import GOKZCN_CHANNEL_ID
from dc_utils.gokzcn import gokzcn_rank
from datetime import datetime


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


async def setup(bot: commands):
    await bot.add_cog(Leaderboards(bot))
