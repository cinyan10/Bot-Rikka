import random
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from query import *
from webhook import *
from pymysql import Connection
from database import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# main_bot.py
intents = discord.Intents.default()
intents.message_content = True

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
    content = str(content)
    result = ''
    if not content:
        for s in servers:
            result += query_server_simple(s)
        await ctx.send(result)
        return

    # query single server info
    try:
        server_id = int(content)
        s = find_server_by_id(server_id)
        result = query_server_details(s)
    except Exception:   # NOQA
        s = find_server_by_name(content)
        result = query_server_details(s)
    await ctx.send(result)


@bot.hybrid_command()
async def servers(ctx):
    await send_webhook()


@bot.hybrid_command()
async def ping(ctx):
    """ping bot"""
    responses = ["meow~", "Itami~ >.<", "What's the matter, gosyujinnsama?", "pong~", "UwU", "don't poke me, plz T^T"]
    result = random.choice(responses)
    await ctx.send(result)


@bot.hybrid_command()
async def bind_steam(ctx, steam_id: str):
    discord_id = ctx.author.id

    # Insert or update user binding in the database
    cursor = connection.cursor()
    cursor.execute(
        'INSERT INTO user_bindings (discord_id, steam_id) '
        'VALUES (%s, %s) ON DUPLICATE KEY UPDATE steam_id = VALUES(steam_id)',
        (discord_id, steam_id)
    )
    connection.commit()
    cursor.close()

    await ctx.send('Steam ID bound successfully!')


print('Bot_Rikka starting...')
bot.run(TOKEN)

