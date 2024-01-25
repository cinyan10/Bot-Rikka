import os
import discord
from discord.ext import commands
from config import TOKEN
import asyncio

discord.utils.setup_logging()

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


async def load():
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            print(f'Loaded {filename}')


async def main():
    await load()
    await bot.start(TOKEN)

asyncio.run(main())
