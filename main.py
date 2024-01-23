from discord.ext import commands
from functions.gokzcn import *
from config import *
import asyncio

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')


async def main():
    await load()
    await bot.start(TOKEN)

asyncio.run(main())
