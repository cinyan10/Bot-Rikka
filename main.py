# main.py
import random
import discord
from discord.ext import commands
from database import *
from query import *
from webhook import *
from config import *

# Constants
COMMAND_PREFIX = "!"

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)


# ----- Command Group: Basic Commands -----
@bot.command()
@commands.has_permissions(administrator=True)
async def sync(ctx):
    await bot.tree.sync()
    await ctx.send("Sync completed!")


@bot.hybrid_command()
async def ping(ctx):
    """ping bot"""
    responses = ["meow~", "Itami~ >.<", "What's the matter, gosyujinnsama?", "pong~", "UwU", "don't poke me, plz T^T"]
    result = random.choice(responses)
    await ctx.send(result)


# ----- Command Group: Server Commands -----


@bot.hybrid_command()
async def server(ctx, content: str = None):   # NOQA
    """query server info by name or id
    Parameters:
        content (str, optional): input the server name(e.g. 广州1) or id. it will show all servers info if it's None
    """
    # if content = None, query all servers info
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
    """get server infos in bot-commands channel as webhook"""
    send_webhook()
    await ctx.send("Server List Sent!")


# ----- Command Group: Utility Commands -----


@bot.hybrid_command()
async def bind_steam(ctx, steam_id: str):
    """bind your steamid32"""
    user_id = ctx.author.id

    # Insert or update user binding in the database
    cursor = connection.cursor()
    connection.select_db('discord')
    cursor.execute(
        'INSERT INTO users (discord_id, steamid_32) '
        'VALUES (%s, %s) ON DUPLICATE KEY UPDATE steamid_32 = VALUES(steamid_32)',
        (user_id, steam_id)
    )
    connection.commit()
    cursor.close()
    await ctx.send('Steam ID bound successfully!')


@bot.hybrid_command()
async def reset_steam(ctx, steamid: str = None):
    """resets the steamid"""
    user_id = ctx.author.id
    reset_user_steam(user_id, steamid)
    await ctx.send('Your Steam ID has been reset.')


@bot.hybrid_command()
async def info(ctx):
    """Shows information aboutyou."""
    user_id = ctx.author.id
    steam_id = retrieve_steam_id(user_id)
    name = retrieve_user_name(steam_id)
    join_date = retrieve_join_date(steam_id)
    last_seen = retrieve_last_seen(steam_id)

    if join_date and last_seen:
        await ctx.send(f'Player: **{name}**\nSteam ID: `{steam_id}`\nJoin Date: {join_date}\nLast Seen: {last_seen}')
    else:
        await ctx.send('No data found for the specified Steam ID.')


# ----- Main Execution -----
print('Bot_Rikka starting...')
bot.run(TOKEN)
