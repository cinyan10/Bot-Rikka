import asyncio
import traceback

import discord
import mysql.connector
from discord import Role, Embed
from discord.ext import commands

from config import *
from functions.database import execute_query, discord_id_to_steamid
from functions.db_operate.db_discord import get_kzmode
from functions.db_operate.db_firstjoin import check_wl
from functions.globalapi.kz_global_stats import *
from functions.steam import convert_steamid
from functions.misc import formate_record_time


class StatsView(discord.ui.View):

    def __init__(self, embeds: list[discord.Embed]):
        super().__init__()
        self.embeds: list = embeds

    def get_embeds(self, label) -> Embed:
        modes = {
            "KZT": self.embeds[0],
            "SKZ": self.embeds[1],
            "VNL": self.embeds[2],
        }
        return modes[label]

    @discord.ui.button(label='KZT', style=discord.ButtonStyle.green)
    async def kz_timer(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=self.get_embeds(button.label))

    @discord.ui.button(label='SKZ', style=discord.ButtonStyle.blurple)
    async def kz_simple(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=self.get_embeds(button.label))

    @discord.ui.button(label='VNL', style=discord.ButtonStyle.gray)
    async def kz_vanilla(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=self.get_embeds(button.label))


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


async def kz_info(ctx, member: discord.Member, steamid):
    ms = await ctx.send(embed=Embed(title="KZ Stats Loading..."))
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

    try:
        embeds = [get_stats_embed(steamid64, kzmode) for kzmode in ['kzt', 'skz', 'vnl']]

    except Exception as e:
        embeds = [Embed(title="Error!", description=str(e), colour=discord.Colour.red())]
    await ms.edit(embeds=embeds, view=StatsView(embeds))


async def personal_recent(ctx, limit, member: discord.Member, steamid, kzmode):
    ms = await ctx.send(embed=Embed(title="Loading..."))
    if member:
        steamid = discord_id_to_steamid(member.id)
        steamid64 = convert_steamid(steamid, 'steamid64')
    elif steamid:
        steamid64 = convert_steamid(steamid, "steamid64")
    else:
        steamid64 = convert_steamid(ctx.author.id, "steamid64")

    records = fetch_personal_recent(steamid64, kzmode, limit)

    embeds = []
    for record in records:
        print("我被执行了")
        embed = Embed(
            title=record['map_name'],
            url=(KZGOEU_MAPS_URL + record['map_name']),
            description=f"Player: {record['player_name']} steamID: {record['steam_id']}",
            timestamp=formate_record_time(record['updated_on'])
        )

        embed.add_field(name="Mode", value=record['mode'])
        embed.add_field(name="Time", value=record['time'])
        embed.add_field(name="Teleports", value=record['teleports'])
        embed.add_field(name="Points", value=record['points'])
        embed.add_field(name="Place", value=record['place'])
        if record['server_name'] == 'C10 GOKZ':
            record['server_name'] = 'AXE GOKZ'
        embed.add_field(name="Server Name", value=record['server_name'])

        embed.set_footer(text="id:"+record['id'])
        embed.set_image(url=f"MAP_IMAGE{record['map_name']}.jpg")

        embeds.append(embed)

    print("Ready to Send", len(embeds))
    await ms.edit(embeds=embeds)

if __name__ == "__main__":

    pass
