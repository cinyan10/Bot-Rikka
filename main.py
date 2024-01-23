from datetime import datetime, timezone
import random
import discord
from discord.ext import commands
from functions.database import *
from functions.embed_content import *
from functions.query import *
from functions.webhook import *
from functions.gokzcn import *
from config import *
import asyncio
from pymysql.err import IntegrityError

# Constants
COMMAND_PREFIX = "!"

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)


async def generic_embed_loop(channel_id, title, update_function, update_interval=60):
    channel = bot.get_channel(channel_id)
    message = await get_or_create_message(channel, title, 'Loading...')
    while True:
        embeds = update_function()
        await message.edit(embeds=embeds)
        await asyncio.sleep(update_interval)


# Function to create or fetch a message in a channel
async def get_or_create_message(channel, title, description):
    async for message in channel.history(limit=1):
        return message
    embed = discord.Embed(title=title, description=description)
    return await channel.send(embed=embed)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.get_channel(PRINT_CHANNEL_ID).send(content="I'm successfully started!!")

    # Tasks for updating embeds
    tasks = [
        generic_embed_loop(SERVER_LIST_CHANNEL_ID, 'AXE SERVER LIST', query_all_servers),
        generic_embed_loop(GUANGZHOU_CHANNEL_ID, '广州 SERVER LIST', lambda: query_server_embed(SERVER_LIST[:6]), 60),
        generic_embed_loop(BEIJING_CHANNEL_ID, '北京 SERVER LIST', lambda: query_server_embed(SERVER_LIST[6:]), 60),
        generic_embed_loop(JSTOP_CLIENT_ID, 'Jumpstats Top', jstop_embed_update, 7200)
    ]
    # Run all tasks concurrently and wait for them to complete
    await asyncio.gather(*tasks)


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


def jstop_embed_update():
    embeds = [get_jstop(20, 'kzt'), get_jstop(10, 'skz'), get_jstop(10, 'vnl')]
    return embeds


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
async def bind_steam(ctx, steamid: str):
    """Bind your steamid, steamid can be any type"""
    user_id = ctx.author.id
    try:
        bind_user_steam(user_id, steamid, ctx)
        await ctx.send('Steam ID bound successfully!')
    except IntegrityError as e:
        # Check for duplicate entry error
        if 'Duplicate entry' in str(e) and 'steamid_32' in str(e):
            await ctx.send('This Steam ID is already bound to another user.')
        else:
            await ctx.send('An error occurred while binding the Steam ID.')
    except Exception as e:
        await ctx.send(f'An unexpected error occurred: {e}')


@bot.hybrid_command()
async def reset_steam(ctx):
    """Resets the steamid"""
    user_id = ctx.author.id
    reset_user_steam(user_id)
    await ctx.send('Your Steam ID has been reset.')


@bot.hybrid_command()
async def gokzcn(ctx, steamid: str = None, mode: str = 'kzt'):
    """Show your gokz.cn info"""
    discord_id = ctx.author.id
    steamid = discordid_to_steamid(discord_id)
    result = get_gokzcn_info(discord_id, mode=mode, steamid=steamid)
    await ctx.send(embed=result)


@bot.hybrid_command()
async def info(ctx, steamid: str = None):
    """Show your information"""
    discord_id = ctx.author.id
    result = user_info(discord_id, steamid)
    await ctx.send(embed=result)

# ----- Main Execution -----
print('Bot_Rikka starting...')
bot.run(TOKEN)
