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
async def info(ctx, num: str):
    """show server info"""

    content = query_server(servers[num][0], servers[num][1])
    await ctx.send(content)


@bot.hybrid_command()
async def info(ctx, content):
    """show server info"""
    try:
        num = int(content)
        content = query_server(servers_dict[num][0], servers[num][1])
    except Exception:
        if content[:1] == '北京':
            num = int(content[2]) + 6
            content = query_server(servers_dict[num][0], servers[num][1])
        elif content[:1] == '广州':
            num = int(content[2])
            content = query_server(servers_dict[num][0], servers[num][1])
    await ctx.send(content)


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
