import discord
from discord.ext import commands

class admin(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._last_member = None

    @commands.command(description="Clears previous messages")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount):
        await ctx.channel.purge(limit=int(amount) + 1)
        await ctx.send('Cleared {} messages'.format(amount), delete_after=5)


def setup(client):
    client.add_cog(admin(client))