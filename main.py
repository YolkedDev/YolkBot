import aiohttp
import aiosqlite
import asyncio
from datetime import datetime as dt
import db_interface
from discord.ext import commands
import json
import os


class YolkBot(commands.Bot):
    """ custom, subclassed bot for all your eggy needs """
    def __init__(self):
        super().__init__(command_prefix=self.get_prefix,
                         case_insensitive=True)
        self.start_time = dt.now()
        self.web, self.db = asyncio.run(self.async_setup())
        self.first_on_ready = True
        self.log_ch = None
        self.team = None

        for ext in os.listdir("cogs"):
            if ext.endswith(".py"):
                self.load_extension(f"cogs.{ext[:-3]}")


    @staticmethod
    async def async_setup():
        web = aiohttp.ClientSession()
        db = await aiosqlite.connect("db/bot.db")

        return web, db


    async def get_prefix(self, message):
        default_prefix = "yolk "

        if message.guild:
            guild_info = await db_interface.get_guild_data(self.db, message.guild.id)
            try:
                return guild_info["info"]["prefix"]
            except (KeyError, TypeError):
                pass

        return default_prefix


    async def on_ready(self):
        print(f"===== ON_READY =====\n"
              f"\tlogged in as:\t{self.user}\n"
              f"\tid:\t\t{self.user.id}\n"
              f"\tdt:\t\t{dt.now()}\n\n")

        if self.first_on_ready:
            self.log_ch = self.get_channel(555065838093336600)
            await self.log_ch.send("bot started")

            team_obj = (await self.application_info()).team
            team = {
                "icon_url": team_obj.icon_url,
                "member_ids": [m.id for m in team_obj.members],
                "name": team_obj.name
            }
            self.team = team
            self.first_on_ready = False     # prevents start msg from sending on random on_ready's


if __name__ == "__main__":
    with open("_keys.json") as f:
        token = json.load(f)["discord"]

    YolkBot().run(token)
