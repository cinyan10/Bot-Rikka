import aiohttp
import discord
from query import *
from servers import *

web_url = "https://discord.com/api/webhooks/1198569911757308026/p8qXZuo5Rhf7e_5VagkGK8uYaG5Gf9WemfWIh7uBpyv1ySRM34NJJ_ZvmyqqbJgdAyf2"


async def send_embedded_webhook(webhook_url, title, description, color=discord.Color.green()):
    print("Before webhook creation")
    async with aiohttp.ClientSession() as session:
        print("After session creation")
        webhook = discord.Webhook.from_url(webhook_url, session=session)
        print("After webhook creation")
        # ... rest of the code

        embed = discord.Embed(
            title=title,
            description=description,
            color=color
        )

        await webhook.send(embed=embed)


async def query_info_and_send_webhook():
    result = ''
    for s in servers:
        try:
            result += await query_server_simple(s)
        except Exception as e:
            result += f"Error querying server {s}: {str(e)}"

    await send_embedded_webhook(web_url, 'Server List', result, color=discord.Color.blue())

# Run the asynchronous function using asyncio
import asyncio
asyncio.run(query_info_and_send_webhook())
