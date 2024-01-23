from discord.ext import commands

from dc_utils.setting import set_language, set_kz_mode


class SettingCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("SettingCommands Cog loaded")

    @commands.hybrid_command(name="setting")
    async def setting(self, ctx, language=None, kz_mode=None):
        """
        Get your lj pb or other's lj pb
        """
        if language:
            await set_language(ctx, language)
        if kz_mode:
            await set_kz_mode(ctx, kz_mode)


async def setup(bot):
    await bot.add_cog(SettingCommands(bot))
