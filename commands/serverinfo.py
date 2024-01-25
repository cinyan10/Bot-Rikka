from discord.ext import commands
from functions.query import query_server_simple, find_server_by_id, find_server_by_name, query_server_details
from functions.servers import SERVER_LIST
from functions.webhook import send_webhook


class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(ServerInfo(bot))
