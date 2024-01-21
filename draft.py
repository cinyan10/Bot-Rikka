import discord
from discord.ext import commands
import database.connector

bot = commands.Bot(command_prefix='!')

# MySQL connection details
db_config = {
    'host': 'your_mysql_host',
    'user': 'your_mysql_user',
    'password': 'your_mysql_password',
    'database': 'your_mysql_database',
}

# Create a MySQL connection
connection = mysql.connector.connect(**db_config)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

@bot.command(name='setconfig')
async def set_config(ctx, steam_id: str, prefer_language: str, other_field1: int, other_field2: str):
    user_id = ctx.author.id

    # Insert or update user configuration in the database
    cursor = connection.cursor()
    cursor.execute(
        'INSERT INTO users (user_id, steam_id, prefer_language, other_field1, other_field2) '
        'VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE '
        'steam_id = VALUES(steam_id), prefer_language = VALUES(prefer_language), '
        'other_field1 = VALUES(other_field1), other_field2 = VALUES(other_field2)',
        (user_id, steam_id, prefer_language, other_field1, other_field2)
    )
    connection.commit()
    cursor.close()

    await ctx.send('Configuration set successfully!')

@bot.command(name='getconfig')
async def get_config(ctx):
    user_id = ctx.author.id

    # Retrieve user configuration from the database
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        'SELECT steam_id, prefer_language, other_field1, other_field2 FROM users WHERE user_id = %s',
        (user_id,)
    )
    result = cursor.fetchone()
    cursor.close()

    if result:
        config_message = f'Your configuration:\n'
        config_message += f'Steam ID: {result["steam_id"]}\n'
        config_message += f'Preferred Language: {result["prefer_language"]}\n'
        config_message += f'Other Field 1: {result["other_field1"]}\n'
        config_message += f'Other Field 2: {result["other_field2"]}\n'
        await ctx.send(config_message)
    else:
        await ctx.send('No configuration found.')

# Run your Discord bot
bot.run('your_discord_bot_token')
