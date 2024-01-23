from discord.ext import commands
from functions.query import query_server_simple, find_server_by_id, find_server_by_name, query_server_details
from functions.servers import SERVER_LIST
from functions.webhook import send_webhook


class ServerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def server(self, ctx, content: str = None):
        """query server info by name or id"""
        # if content = None, query all SERVER_LIST info
        result = ''
        if not content:
            for s in SERVER_LIST:
                result += query_server_simple(s)
            await ctx.send(result)
            return

        # query single server info
        try:
            server_id = int(content)
            s = find_server_by_id(server_id)
            result = query_server_details(s)
        except Exception:  # NOQA
            s = find_server_by_name(content)
            result = query_server_details(s)
        await ctx.send(result)

    @commands.hybrid_command()
    async def servers(self, ctx):
        """get server infos in bot-cogs channel as webhook"""
        send_webhook()
        await ctx.send("Server List Sent!")


async def setup(bot):
    await bot.add_cog(ServerCommands(bot))
