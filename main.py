from config import *
import asyncio
from dc_utils.announcement import *


# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
bot = PersistentViewBot()
discord.utils.setup_logging()


# Loading Modules
async def load():
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            await bot.load_extension(f'commands.{filename[:-3]}')
            print(f'Loaded {filename[:-3]}')


async def main():
    await load()
    await bot.start(TOKEN)

asyncio.run(main())
