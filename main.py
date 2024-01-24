import os
import discord
from discord.ext import commands
from config import TOKEN
import asyncio

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')


load_cogs()
bot.run(TOKEN)
