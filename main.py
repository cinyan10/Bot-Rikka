import random
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from query import *
from servers import *

# discord initial
intents = discord.Intents.default()
intents.message_content = True
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix="!", intents=intents)


# functions
@bot.command()
@commands.has_permissions(administrator=True)
async def sync(ctx):
    await bot.tree.sync()
    await ctx.send("Sync completed!")


@bot.hybrid_command()
async def info(ctx, content: str = None):   # NOQA
    """query server info by name or id
    Parameters:
        content (str, optional): input the server name(e.g. 广州1) or id. it will show all servers info if it's None
    """
    # if content = None, query all servers info
    result = ''
    if not content:
        for s in servers:
            result += query_server_basic(s)
        await ctx.send(result)
        return

    # query single server info
    try:
        server_id = int(content)
        s = find_server_by_id(server_id)
        result = query_server(s)
    except Exception:   # NOQA
        s = find_server_by_name(content)
        result = query_server(s)
    await ctx.send(result)


@bot.hybrid_command()
async def ping(ctx):
    """ping bot"""
    responses = ["meow~", "Itami~ >.<", "What's the matter, gosyujinnsama?", "pong~", "UwU", "don't poke me, plz T^T"]
    result = random.choice(responses)
    await ctx.send(result)


bot.run(TOKEN)
