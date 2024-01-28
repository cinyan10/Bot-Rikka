import discord
from discord.ext import commands
from config import *
import asyncio


# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
discord.utils.setup_logging()


async def load():
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            await bot.load_extension(f'commands.{filename[:-3]}')
            print(f'Loaded {filename[:-3]}')


async def main():
    await load()
    await bot.start(TOKEN)

asyncio.run(main())
