
import datetime
import sys
import discord
from redbot.core import (
    __version__,
    version_info as red_version_info,
    commands,
)
from discord_components import DiscordComponents, Button

from .utils._internal_utils import fetch_latest_red_version_info
from .utils.chat_formatting import box


_info = None

class Info(commands.Cog):
    """info bot to your server."""

    __version__ = "1.0.0"

    def __init__(self, bot):
        self.bot = bot

    def cog_unload(self):
        global _info
        if _info:
            try:
                self.bot.remove_command("info")
            except:
                pass
            self.bot.add_command(_info)

    @commands.command(aliases=['stats'])
    async def info(self, ctx: commands.Context):
        """Shows info about [botname]."""
        embed_links = await ctx.embed_requested()
        author_repo = "https://github.com/Twentysix26"
        org_repo = "https://github.com/Cog-Creators"
        red_repo = org_repo + "/Red-DiscordBot"
        red_pypi = "https://pypi.org/project/Red-DiscordBot"
        support_server_url = "https://discord.gg/red"
        dpy_repo = "https://github.com/Rapptz/discord.py"
        python_url = "https://www.python.org/"
        since = datetime.datetime(2016, 1, 2, 0, 0)
        days_since = (datetime.datetime.utcnow() - since).days

        app_info = await self.bot.application_info()
        if app_info.team:
            owner = app_info.team.name
        else:
            owner = app_info.owner
        custom_info = await self.bot._config.custom_info()

        pypi_version, py_version_req = await fetch_latest_red_version_info()
        outdated = pypi_version and pypi_version > red_version_info
        action_row = [ Button(label='Invite', style=5, url=f'https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot+applications.commands', emoji='<:invite:981441189460975646>'), Button(label='Support', style=5, url='https://discord.gg/elegant', emoji='<:support:981441709588242432>') ]
        if embed_links:
            dpy_version = "[{}]({})".format(discord.__version__, dpy_repo)
            python_version = "[{}.{}.{}]({})".format(*sys.version_info[:3], python_url)
            red_version = "[{}]({})".format(__version__, red_pypi)

            about = (
                "This bot is an instance of [Red, an open source Discord bot]({}) "
                "created by [Twentysix]({}) and [improved by many]({}).\n\n"
                "Red is backed by a passionate community who contributes and "
                "creates content for everyone to enjoy. [Join us today]({}) "
                "and help us improve!\n\n"
                "(c) Cog Creators"
            ).format(red_repo, author_repo, org_repo, support_server_url)

            embed = discord.Embed(color=(await ctx.embed_colour()))
            embed.add_field(
                name=("Instance owned by team") if app_info.team else ("Instance owned by"),
                value=f'[{owner}](https://discordapp.com/users/{owner.id})',
            )
            embed.add_field(name="Python", value=python_version)
            embed.add_field(name="discord.py", value=dpy_version)
            embed.add_field(name=("Red version"), value=red_version)
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            if outdated in (True, None):
                if outdated is True:
                    outdated_value = ("Yes, {version} is available.").format(
                        version=str(pypi_version)
                    )
                else:
                    outdated_value = ("Checking for updates failed.")
                embed.add_field(name="Outdated", value=outdated_value)
            if custom_info:
                embed.add_field(name=(f"About {self.bot.user.name}"), value=custom_info, inline=False)
            embed.add_field(name=("About Red"), value=about, inline=False)

            embed.set_footer(
                text=("Bringing joy since 02 Jan 2016 (over {} days ago!)").format(days_since)
            )
            await ctx.send(embed=embed, components=action_row)
        else:
            python_version = "{}.{}.{}".format(*sys.version_info[:3])
            dpy_version = "{}".format(discord.__version__)
            red_version = "{}".format(__version__)

            about = (
                "This bot is an instance of Red, an open source Discord bot (1) "
                "created by Twentysix (2) and improved by many (3).\n\n"
                "Red is backed by a passionate community who contributes and "
                "creates content for everyone to enjoy. Join us today (4) "
                "and help us improve!\n\n"
                "(c) Cog Creators"
            )
            about = box(about)

            if app_info.team:
                extras = (
                    "Instance owned by team: [{owner}]\n"
                    "Python:                 [{python_version}] (5)\n"
                    "discord.py:             [{dpy_version}] (6)\n"
                    "Red version:            [{red_version}] (7)\n"
                ).format(
                    owner=owner,
                    python_version=python_version,
                    dpy_version=dpy_version,
                    red_version=red_version,
                )
            else:
                extras = (
                    "Instance owned by: [{owner}]\n"
                    "Python:            [{python_version}] (5)\n"
                    "discord.py:        [{dpy_version}] (6)\n"
                    "Red version:       [{red_version}] (7)\n"
                ).format(
                    owner=owner,
                    python_version=python_version,
                    dpy_version=dpy_version,
                    red_version=red_version,
                )

            if outdated in (True, None):
                if outdated is True:
                    outdated_value = ("Yes, {version} is available.").format(
                        version=str(pypi_version)
                    )
                else:
                    outdated_value = ("Checking for updates failed.")
                extras += ("Outdated:          [{state}]\n").format(state=outdated_value)

            red = (
                ("**About Red**\n")
                + about
                + "\n"
                + box(extras, lang="ini")
                + "\n"
                + ("Bringing joy since 02 Jan 2016 (over {} days ago!)").format(days_since)
                + "\n\n"
            )

            await ctx.send(red)
            if custom_info:
                custom_info = ("**About this instance**\n") + custom_info + "\n\n"
                await ctx.send(custom_info)
            refs = (
                "**References**\n"
                "1. <{}>\n"
                "2. <{}>\n"
                "3. <{}>\n"
                "4. <{}>\n"
                "5. <{}>\n"
                "6. <{}>\n"
                "7. <{}>\n"
            ).format(
                red_repo, author_repo, org_repo, support_server_url, python_url, dpy_repo, red_pypi
            )
            await ctx.send(refs)

async def setup(bot):
    _info = bot.get_command("info")
    DiscordComponents(bot)
    if _info:
        bot.remove_command(_info.name)
    bot.add_cog(Info(bot))