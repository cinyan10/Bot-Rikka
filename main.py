from discord.ext import commands
import asyncio
from functions.gokzcn import *
from config import *

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Load cogs
initial_extensions = [f'cogs.{filename[:-3]}' for filename in os.listdir('./cogs') if filename.endswith('.py')]

for extension in initial_extensions:
    try:
        bot.load_extension(extension)
    except Exception as e:
        print(f'Failed to load extension {extension}: {str(e)}')


async def main():
    await bot.start(TOKEN)

asyncio.run(main())
