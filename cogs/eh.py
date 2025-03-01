from discord.ext import commands
import traceback as tb


class EH(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if hasattr(ctx.command, "on_error"):
            return

        error = getattr(error, "original", error)

        with open("log.txt", "a+", encoding="utf16") as f:
            f.write(f"""--- {error}
            {ctx.author} - {ctx.author.id}
            {ctx.message.content}
            {tb.extract_tb(error.__traceback__)}\n\n""")

        em_dict = {
            commands.ExtensionNotFound: "The extension was not found.",
            commands.ExtensionAlreadyLoaded: "The extension is already loaded.",
            commands.NoEntryPointError: "The extension does not have a setup function.",
            commands.ExtensionFailed: "The extension or its setup function had an execution error.",
            commands.ExtensionNotLoaded: "That extension is not loaded.",

            commands.UserInputError: "Hmm... Something you entered wasn't quite right. Try `help [command]`.",
            commands.NotOwner: "Only the owner of the bot can use this command.",
            commands.NoPrivateMessage: "This command can't be used outside of a server.",
        }

        await ctx.message.add_reaction("\U0000274e")

        if isinstance(error, commands.CommandNotFound):
            return

        for e in em_dict:
            if isinstance(error, e):
                await ctx.send(em_dict[e])
                return

        if isinstance(error, commands.CheckFailure):
            if hasattr(ctx, "custom_check_fail"):
                msg = ctx.custom_check_fail
            else:
                msg = "The requirements to run this command were not satisfied."
            await ctx.send(msg)
            return

        await ctx.send(tb.extract_tb(error.__traceback__), delete_after=10)
        raise error


def setup(bot):
    bot.add_cog(EH(bot))
