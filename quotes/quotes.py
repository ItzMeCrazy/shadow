from typing import Optional
import aiohttp
import discord
from redbot.core import commands


class Quotes(commands.Cog):
    """Fetch quotes from an api."""

    __version__ = "1.0.0"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["qotd"])
    async def quoteoftheday(self, ctx: commands.Context) -> None:
        """Displays the device user is using."""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://quotes.rest/qod?language=en",
                headers={"accept": "application/json"},
            ) as resp:
                if resp.status == 200:
                    json_response = await resp.json()
                    quote = json_response["contents"]["quotes"][0]["quote"]
                    embed = discord.Embed(title="Quote of the day!", color=0x2F3136)
                    embed.description = quote
                    embed.set_author(
                        name=ctx.author.name, icon_url=ctx.author.avatar_url
                    )
                    embed.set_footer(name=ctx.guild.name, value=ctx.guild.icon_url)
                    await ctx.send(embed=embed)
