import discord
from discord.ext import commands
from main import YolkBot
from typing import Optional, Union


class Admin(commands.Cog):
    def __init__(self, bot: YolkBot):
        self.bot = bot
        self.log_details = {
            "ban": [discord.Colour.red(), "banned"],
            "unban": [discord.Colour.light_grey(), "unbanned"],
            "purge": [discord.Colour.orange(), "purged"]
        }

    @commands.Cog.listener()
    async def on_admin_action(self, ctx, *, action: str,
                              target: Union[discord.Member, discord.User, discord.TextChannel], reason: str):
        embed = discord.Embed(colour=self.log_details[action][0])
        embed.set_author(name="\u200B", icon_url=ctx.author.avatar_url)
        embed.add_field(name=action.title(),
                        value=f"**{target.mention}** was {self.log_details[action][1]} "
                              f"by {ctx.author.mention}")
        embed.set_footer(text=reason)

        modlog_channel = self.bot.get_channel(self.bot.modlog_id)
        await modlog_channel.send(embed=embed)
        await ctx.send(embed=embed, delete_after=7)


    @commands.command(description="Bans the target user/member from the server.",
                      brief="Requires Ban Members permission.")
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.User, *, reason):
        await ctx.guild.ban(user, reason=reason)
        self.bot.dispatch("admin_action", ctx, action="ban", target=user, reason=reason)


    @commands.command(description="Unbans the target user/member from the server.",
                      brief="Requires Ban Members permission.")
    @commands.has_guild_permissions(ban_members=True)
    async def unban(self, ctx, user: discord.User, *, reason):
        await ctx.guild.unban(user, reason=reason)
        self.bot.dispatch("admin_action", ctx, action="unban", target=user, reason=reason)


    @commands.command(description="For purging messages. You may specify an author and/or "
                                  "an end-point message (messages sent after this message will "
                                  "be checked). Note that `number` is the number of messages to check.",
                      brief="Requires Manage Messages permission (guild-wide).",
                      aliases=["clear"])
    @commands.has_guild_permissions(manage_messages=True)
    async def purge(self, ctx, number: int,
                    author: Optional[Union[discord.Member, discord.User]] = None,
                    after: discord.Message = None):
        if number not in range(3, 151):
            return await ctx.send("Number of messages to check must be between 3 and 150 inclusive.")

        def check(msg):
            if author is not None:
                return msg.author.id == author.id
            return True

        await ctx.message.delete()
        msgs = await ctx.channel.purge(limit=number, check=check, after=after)
        self.bot.dispatch("admin_action", ctx, action="purge", target=ctx.channel,
                          reason=f"{len(msgs)} messages purged.")


def setup(bot):
    bot.add_cog(Admin(bot))
