from discord import Embed, Message
from discord.ext import commands
from config import GOKZCN_CHANNEL_ID
from dc_utils.gokzcn import gokzcn_rank


class Leaderboards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Leaderboards Cog loaded')

    @commands.hybrid_command()
    async def update_gokzcn_rank(self, ctx):
        """update the gokzcn_rank in channel"""
        channel = self.bot.get_channel(GOKZCN_CHANNEL_ID)

        send_ms: Message = await ctx.send(embed=Embed(title="Loading...", description=f"this will take a while...", color=0x60FFFF))
        last_message = None
        try:
            # Get the channel by channel ID

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
                await send_ms.edit(embed=Embed(title="Done", description=f"Ranking send in {channel.name}", color=0x60FFFF))
            else:
                # If there is an existing message, edit it
                await last_message.edit(content='', embed=content)
                await send_ms.edit(embed=Embed(title="Done", description=f"Ranking updated in {channel.name}", color=0x60FFFF))

        except Exception as e:
            await send_ms.edit(embed=Embed(title="Error", description=f"{e}", color=0x60FFFF))


async def setup(bot: commands):
    await bot.add_cog(Leaderboards(bot))
