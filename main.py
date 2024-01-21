import random
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from query import *

intents = discord.Intents.default()
intents.message_content = True
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.command()
@commands.has_permissions(administrator=True)
async def sync(ctx):
    await bot.tree.sync()
    await ctx.send("Synchronization completed!")


@bot.hybrid_command()
async def info_id(ctx, num: int):
    """show server info by num"""
    result = query_server(servers[num][0], servers[num][1])
    await ctx.send(result)


@bot.hybrid_command()
async def info(ctx, content: str = None):
    """show server info by name"""
    result = ''
    if not content:
        for server in servers:
            result += query_server_basic(server[0], server[1])
    try:
        num = int(content) - 1
        result = query_server(servers[num][0], servers[num][1])
    except Exception:
        if content[:2] == '北京':
            num = int(content[2]) + 5
            result = query_server(servers[num][0], servers[num][1])
        elif content[:2] == '广州':
            num = int(content[2]) - 1
            result = query_server(servers[num][0], servers[num][1])
    await ctx.send(result)


@bot.hybrid_command()
async def ping(ctx):
    """ping bot"""
    num = random.randint(1, 6)
    if num == 1:
        await ctx.send("meow~")
    elif num == 2:
        await ctx.send("Itami~ >.<")
    elif num == 3:
        await ctx.send("What's the matter, gosyujinnsama?")
    elif num == 4:
        await ctx.send("pong~")
    elif num == 5:
        await ctx.send("UwU")
    else:
        await ctx.send("don't poke me again plz T^T ")


bot.run(TOKEN)
