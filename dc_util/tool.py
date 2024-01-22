# TOOL PACKAGE
import discord


async def get_or_send_message(channel) -> discord.Message:
    # Retrieve the last message in the channel
    messages = await channel.history(limit=1).flatten()

    if messages:
        # If messages exist, return the last message
        return messages[0]
    else:
        # If no messages exist, send a new message with 'Loading' content
        new_message = await channel.send("Loading...")
        return new_message
