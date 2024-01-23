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

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        coro = bot.load_extension(f'cogs.{filename[:-3]}')
        asyncio.run(coro)

bot.run(TOKEN)
