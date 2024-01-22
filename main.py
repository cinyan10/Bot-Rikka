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


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

    # Fetch the channel using the stored channel ID
    channel = bot.get_channel(SERVER_LIST_CHANNEL_ID)

    # Check if a message already exists in the channel
    async for message in channel.history(limit=1):
        # If there's an existing message, use that message for the loop
        existing_message = message
        break
    else:
        # If no existing message, send a new one and use that for the loop
        embed = discord.Embed(title='AXE SERVER LIST', description='Loading')
        existing_message = await channel.send(embed=embed)

    # Start the dynamic embed loop
    await dynamic_embed_loop(existing_message)


# ---- Loop
async def dynamic_embed_loop(message):
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
@bot.command()
async def send_six_embeds(ctx):
    # Create a list to store the embeds
    embeds = []
    # Create six embeds and add them to the list
    for s in server_list[:7]:
        embed = query_server_embed(s)
        embeds.append(embed)

    # Get the channel using its ID
    destination_channel = bot.get_channel(GUANGZHOU_CHANNEL_ID)
    # Remove any potential None values from the embeds list
    embeds = [e for e in embeds if e]
    # Send the list of embeds as a single message
    await destination_channel.send(embeds=embeds)

# Replace DESTINATION_CHANNEL_ID, 'author_icon_url', 'https://example.com/embed_url', and 'image_url' with the actual values


@bot.hybrid_command()
async def server(ctx, content: str = None):   # NOQA
    """query server info by name or id
    Parameters:
        content (str, optional): input the server name(e.g. 广州1) or id. it will show all server_list info if it's None
    """
    # if content = None, query all server_list info
    result = ''
    if not content:
        for s in server_list:
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
