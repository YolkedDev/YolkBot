from datetime import datetime as dt
import db_interface
from discord.ext import commands
import other.custom_checks as checks


class ServerTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @staticmethod
    async def guild_setup(db, guild):
        info = {'info': {'name': guild.name, 'join': str(dt.now().strftime(f'%d/%m/%Y'))}}
        await db_interface.dump_guild_data(db, guild.id, info)


    @commands.command(description="Resets ALL the data stored by the bot about the guild. "
                                  "Use with caution.",
                      brief="Administrator permission required.")
    @commands.has_guild_permissions(administrator=True)
    async def reset_guild_data(self, ctx):
        await self.guild_setup(self.bot.db, ctx.guild)
        await ctx.send('Guild data has been reset.')


    @commands.command(description="Set a custom command prefix for this guild.",
                      brief="Manage Server permission required.")
    @commands.has_guild_permissions(manage_guild=True)
    async def set_prefix(self, ctx, *, prefix: str = ""):
        if prefix == "":
            await ctx.send("Please enter a custom command prefix. E.g.: `set_prefix !`")
        else:
            guild_info = await db_interface.get_guild_data(self.bot.db, ctx.guild.id)
            guild_info['info']['prefix'] = prefix
            await db_interface.dump_guild_data(self.bot.db, ctx.guild.id, guild_info)

            await ctx.send(f"Prefix set to: `{prefix}`")


def setup(bot):
    bot.add_cog(ServerTools(bot))
