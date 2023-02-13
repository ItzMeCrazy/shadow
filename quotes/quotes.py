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
        """Shows quote of the day."""
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
                    embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
                    await ctx.send(embed=embed)

    @commands.command()
    async def quote(self, ctx: commands.Context) -> None:
        """Shows a random quote"""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://quotes.rest/quote/random?language=en&limit=1",
                headers={"accept": "application/json"},
            ) as resp:
                if resp.status == 200:
                    json_response = await resp.json()
                    quote = json_response["contents"]["quotes"][0]["quote"]
                    embed = discord.Embed(title="Random Quote!", color=0x2F3136)
                    embed.description = quote
                    embed.set_author(
                        name=ctx.author.name, icon_url=ctx.author.avatar_url
                    )
                    embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
                    await ctx.send(embed=embed)
