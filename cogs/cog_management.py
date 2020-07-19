from discord.ext import commands
from main import YolkBot
from other.custom_checks import is_on_team


class CogManagement(commands.Cog):
    def __init__(self, bot: YolkBot):
        self.bot = bot

    @commands.command()
    @commands.check(is_on_team)
    async def load(self, ctx, cog_name):
        if cog_name == "cog_management":
            return await ctx.send("can't load cog cog")
        self.bot.load_extension(f"cogs.{cog_name}")

        await ctx.message.add_reaction("\U00002705")
        log_ch = self.bot.get_channel(self.bot.modlog_id)
        await log_ch.send(f"{ctx.author} loaded a cog (`{cog_name}`)")


    @commands.command()
    @commands.check(is_on_team)
    async def reload(self, ctx, cog_name):
        if cog_name == "cog_management":
            return await ctx.send("can't reload cog cog")
        self.bot.reload_extension(f"cogs.{cog_name}")

        await ctx.message.add_reaction("\U00002705")
        log_ch = self.bot.get_channel(self.bot.modlog_id)
        await log_ch.send(f"{ctx.author} reloaded a cog (`{cog_name}`)")


    @commands.command()
    @commands.check(is_on_team)
    async def unload(self, ctx, cog_name):
        if cog_name == "cog_management":
            return await ctx.send("can't unload cog cog")
        self.bot.unload_extension(f"cogs.{cog_name}")

        await ctx.message.add_reaction("\U00002705")
        log_ch = self.bot.get_channel(self.bot.modlog_id)
        await log_ch.send(f"{ctx.author} unloaded a cog (`{cog_name}`)")


def setup(bot):
    bot.add_cog(CogManagement(bot))
