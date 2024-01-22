# main.py
from datetime import datetime, timezone
import random

import discord
from discord.ext import commands
from database import *
from query import *
from webhook import *
from config import *
import asyncio

# Constants
COMMAND_PREFIX = "!"

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)


# AUTO FUNCTIONS
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

    # Fetch the channel using the stored channel ID
    server_list_channel = bot.get_channel(SERVER_LIST_CHANNEL_ID)
    guangzhou_channel = bot.get_channel(GUANGZHOU_CHANNEL_ID)
    beijing_channel = bot.get_channel(BEIJING_CHANNEL_ID)

    # Check if a message already exists in the channel
    async for message in server_list_channel.history(limit=1):
        # If there's an existing message, use that message for the loop
        existing_message = message
        break
    else:
        # If no existing message, send a new one and use that for the loop
        embed = discord.Embed(title='AXE SERVER LIST', description='Loading...')
        existing_message = await server_list_channel.send(embed=embed)

    async for message_2 in guangzhou_channel.history(limit=1):
        # If there's an existing message, use that message for the loop
        existing_message_2 = message_2
        break
    else:
        # If no existing message, send a new one and use that for the loop
        embed = discord.Embed(title='广州 SERVER LIST', description='Loading...')
        existing_message_2 = await guangzhou_channel.send(embed=embed)

    async for message_3 in beijing_channel.history(limit=1):
        # If there's an existing message, use that message for the loop
        existing_message_3 = message_3
        break
    else:
        # If no existing message, send a new one and use that for the loop
        embed = discord.Embed(title='北京 SERVER LIST', description='Loading...')
        existing_message_3 = await beijing_channel.send(embed=embed)

    # Start the dynamic embed loop
    await server_list_embed_loop(existing_message)

    await gz_server_embeds_loop(existing_message_2)
    await gz_server_embeds_loop(existing_message_3)


async def server_list_embed_loop(message):
    while True:
        # Function that updates the content of the embedded message
        current_datetime = datetime.now(timezone.utc)
        new_content = query_all_servers()
        embed = discord.Embed(
            title='AXE SERVER LIST',
            description=new_content,
            colour=0x60FFFF,
            timestamp=current_datetime
        )

        # Edit the embedded message with the new content
        await message.edit(embed=embed)

        # Wait for one minute before the next update
        await asyncio.sleep(60)


async def gz_server_embeds_loop(message: discord.Message):
    embeds = []
    while True:
        for s in SERVER_LIST[:6]:
            embed = query_server_embed(s)
            embeds.append(embed)

        await message.edit(embeds=embeds)
        await asyncio.sleep(60)


async def bj_server_embeds_loop(message: discord.Message):
    embeds = []
    while True:
        for s in SERVER_LIST[6:]:
            embed = query_server_embed(s)
            embeds.append(embed)

        await message.edit(embeds=embeds)
        await asyncio.sleep(60)


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
        content (str, optional): input the server name(e.g. 广州1) or id. it will show all SERVER_LIST info if it's None
    """
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
