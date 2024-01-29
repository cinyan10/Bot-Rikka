# This example requires the 'message_content' privileged intent to function.
from __future__ import annotations

import datetime

import os
from discord import Embed
from discord.ext import commands
import discord
import dotenv


# Define a simple View that persists between bot restarts
# In order for a view to persist between restarts it needs to meet the following conditions:
# 1) The timeout of the View has to be set to None
# 2) Every item in the View has to have a custom_id set
# It is recommended that the custom_id be sufficiently unique to
# prevent conflicts with other buttons the bot sends.
# For this example the custom_id is prefixed with the name of the bot.
# Note that custom_ids can only be up to 100 characters long.
class AnnouncementView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.embeds = [
            Embed(title="Announcement",
                  description="This is English text",
                  color=discord.Color.green(),
                  timestamp=datetime.datetime.now()
                  ),
            Embed(title="公告",
                  description="这是一个中文的公告",
                  color=discord.Color.green(),
                  timestamp=datetime.datetime.now()
                  ),
            Embed(title="公告",
                  description="這是一個中文的公告",
                  color=discord.Color.green(),
                  timestamp=datetime.datetime.now()
                  )
        ]

    @discord.ui.button(label='English', style=discord.ButtonStyle.gray, custom_id='persistent_view:green', emoji='🇬🇧')
    async def green(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=self.embeds[0])  # NOQA

    @discord.ui.button(label='简体中文', style=discord.ButtonStyle.blurple, custom_id='persistent_view:red', emoji="🇨🇳")
    async def red(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=self.embeds[1])  # NOQA

    @discord.ui.button(label='繁體中文', style=discord.ButtonStyle.grey, custom_id='persistent_view:grey', emoji='🇹🇼')
    async def grey(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=self.embeds[2])  # NOQA


class PersistentViewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix=commands.when_mentioned_or('!'), intents=intents)

    async def setup_hook(self) -> None:
        # Register the persistent view for listening here.
        # Note that this does not send the view to any message.
        # In order to do this you need to first send a message with the View, which is shown below.
        # If you have the message_id you can also pass it as a keyword argument, but for this example
        # we don't have one.
        self.add_view(AnnouncementView())
        # For dynamic items, we must register the classes instead of the views.
        # self.add_dynamic_items(DynamicButton)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')


# @bot.command()
# @commands.is_owner()
# async def prepare(ctx: commands.Context):
#     """Starts a persistent view."""
#     # In order for a persistent view to be listened to, it needs to be sent to an actual message.
#     # Call this method once just to store it somewhere.
#     # In a more complicated program you might fetch the message_id from a database for use later.
#     # However, this is outside the scope of this simple example.
#     await ctx.send("What's your favourite colour?", view=AnnouncementView())


if __name__ == '__main__':
    dotenv.load_dotenv()

    TOKEN = os.getenv('TEST_TOKEN')

    bot = PersistentViewBot()

    bot.run(TOKEN)
