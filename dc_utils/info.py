import asyncio

import discord
import mysql.connector
from discord import Role, Embed

from config import db_config, WL_ROLE_ID
from functions.database import execute_query, discord_id_to_steamid
from functions.db_operate.db_discord import get_kzmode
from functions.db_operate.db_firstjoin import check_wl
from functions.globalapi.kz_global_stats import KzGlobalStats
from functions.steam import convert_steamid


def set_bili(ctx, bili_uid) -> str:
    discord_id = ctx.author.id
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    try:
        update_query = "UPDATE discord.users SET bili_uid = %s WHERE discord_id = %s"

        cursor.execute(update_query, (bili_uid, discord_id))

        conn.commit()

        if cursor.rowcount > 0:
            return f"Bili_uid updated for Discord user {discord_id}"
        else:
            return f"Discord user {discord_id} not found in the database. Please /bind_steam first"

    except mysql.connector.Error as err:
        return f"Error: {err}"
    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()


def set_steam(ctx, steam_id):
    username = ctx.author.name  # This gets the user's Discord name
    discord_id = ctx.author.id
    # Check if the SteamID is already bound to another user
    existing_user_query = 'SELECT discord_id FROM discord.users WHERE steamid = %s AND discord_id != %s'
    existing_user_id = execute_query(existing_user_query, (steam_id, discord_id), fetch_one=True)

    if existing_user_id:
        existing_user = ctx.bot.get_user(existing_user_id[0])
        message = f"The SteamID is already bound to {existing_user.mention}" if existing_user else "The SteamID is already bound to another user."
        asyncio.create_task(ctx.send(message))
        return

    # Convert SteamID to different formats
    steamid32 = convert_steamid(steam_id, 'steamid32')
    steamid64 = convert_steamid(steam_id, 'steamid64')
    steamid = convert_steamid(steam_id, 'steamid')

    # Insert or update the user's data in the database
    insert_query = '''
        INSERT INTO discord.users (discord_id, steamid, steamid32, steamid64, username) 
        VALUES (%s, %s, %s, %s, %s) 
        ON DUPLICATE KEY UPDATE 
        steamid = VALUES(steamid), 
        steamid32 = VALUES(steamid32), 
        steamid64 = VALUES(steamid64),
        username = VALUES(username)
    '''
    execute_query(insert_query, (discord_id, steamid, steamid32, steamid64, username), commit=True)
    # Send a confirmation message


async def set_wl_role(ctx, steamid=None):
    role: Role = discord.utils.get(ctx.guild.roles, id=WL_ROLE_ID)
    if steamid:
        member = ctx.author
        if check_wl(steamid):
            await member.add_roles(role)
            await ctx.send(embed=discord.Embed(title="Added AXE Member for you!", colour=discord.Colour.green()))
        else:
            await ctx.send(embed=discord.Embed(title="You haven't been whitelisted yet!", colour=discord.Colour.blue()))
    else:
        pass


async def kz_info(self, ctx, member: discord.Member, steamid, mode):
    ms = await ctx.send(embed=Embed(title="KZ Stats Loading..."))

    discord_id = None
    if member:
        # @mention member
        steamid = discord_id_to_steamid(member.id)
        steamid64 = convert_steamid(steamid, 'steamid64')
    elif steamid:
        steamid64 = convert_steamid(steamid, "steamid64")
    else:
        discord_id = ctx.author.id
        steamid = discord_id_to_steamid(discord_id)
        steamid64 = convert_steamid(steamid, "steamid64")

    if not mode:
        try:
            mode = get_kzmode(discord_id)
        except Exception:
            mode = 'kz_timer'

    try:
        embed = KzGlobalStats(steamid64, kzmode=mode).embed_stats()
    except Exception as e:
        embed = Embed(title="Error!", description=str(e), colour=discord.Colour.red())
    await ms.edit(embed=embed)
