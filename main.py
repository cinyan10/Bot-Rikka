from datetime import datetime, timezone
import random
import discord
from discord.ext import commands
from functions.database import *
from functions.embed_content import *
from functions.query import *
from functions.webhook import *
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
    await bot.get_channel(PRINT_CHANNEL_ID).send(content="I'm successfully started!!")

    async def sync(ctx):
        """s"""
        await bot.tree.sync()
        await bot.get_channel(PRINT_CHANNEL_ID).send(content="Sync completed!")

    # Fetch the channel using the stored channel ID
    server_list_channel = bot.get_channel(SERVER_LIST_CHANNEL_ID)
    guangzhou_channel = bot.get_channel(GUANGZHOU_CHANNEL_ID)
    beijing_channel = bot.get_channel(BEIJING_CHANNEL_ID)

    # Check if a message already exists in the channel
    existing_message = await get_or_create_message(server_list_channel, 'AXE SERVER LIST', 'Loading...')
    existing_message_2 = await get_or_create_message(guangzhou_channel, '广州 SERVER LIST', 'Loading...')
    existing_message_3 = await get_or_create_message(beijing_channel, '北京 SERVER LIST', 'Loading...')

    # Start the dynamic embed loop
    loop_task_1 = asyncio.create_task(server_list_embed_loop(existing_message))
    loop_task_2 = asyncio.create_task(gz_server_embeds_loop(existing_message_2, SERVER_LIST[:6]))
    loop_task_3 = asyncio.create_task(bj_server_embeds_loop(existing_message_3, SERVER_LIST[6:]))

    # Wait for all loop tasks to complete
    await loop_task_1
    await loop_task_2
    await loop_task_3


async def get_or_create_message(channel, title, description):
    async for message in channel.history(limit=1):
        # If there's an existing message, use that message
        return message

    # If no existing message, send a new one
    embed = discord.Embed(title=title, description=description)
    return await channel.send(embed=embed)


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


async def gz_server_embeds_loop(message: discord.Message, servers):
    while True:
        embeds = [query_server_embed(s) for s in servers]
        await message.edit(embeds=embeds)
        await asyncio.sleep(60)


async def bj_server_embeds_loop(message: discord.Message, servers):
    while True:
        embeds = [query_server_embed(s) for s in servers]
        await message.edit(embeds=embeds)
        await asyncio.sleep(60)


# ----- Command Group: Basic Commands -----


@bot.command()
@commands.has_permissions(administrator=True)
async def sync(ctx):
    """s"""
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
    """Show your information"""
    discord_id = ctx.author.id
    result = user_info(discord_id)
    await ctx.send(embed=result)

# ----- Main Execution -----
print('Bot_Rikka starting...')
bot.run(TOKEN)
