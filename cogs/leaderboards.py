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
        try:
            channel = self.bot.get_channel(GOKZCN_CHANNEL_ID)
            if channel is None:
                await ctx.send(f"Channel with ID {GOKZCN_CHANNEL_ID} not found.")
                return

            # Try to fetch the last message in the channel
            last_message = await channel.history(limit=1).flatten()

            # Get the content from the gokzcn_rank() function
            content = gokzcn_rank()

            if not last_message:
                # If there are no messages, send a new message
                await channel.send(content)
                await ctx.send(f"Rank send in #{channel.name}.")
            else:
                # If there is an existing message, edit it
                await last_message[0].edit(content=content)
                await ctx.send(f"Rank updated in #{channel.name}.")

        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")


async def setup(bot: commands):
    await bot.add_cog(Leaderboards(bot))
