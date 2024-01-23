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


# Define 'load' as an async function
async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and not filename.startswith('__'):
            cog_name = f'cogs.{filename[:-3]}'
            try:
                await bot.load_extension(cog_name)
            except commands.ExtensionFailed as e:
                print(f'Failed to load extension {cog_name}: {e}')


async def main():
    await load()
    await bot.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main())
