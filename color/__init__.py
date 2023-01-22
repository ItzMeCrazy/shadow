
from typing import Optional
import aiohttp
import discord
from redbot.core import commands

class Color(commands.Cog):
    """Finds color as per given hex."""

    __version__ = "1.0.0"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["colour"])
    @commands.bot_has_permissions(embed_links=True)
    async def color(self, ctx: commands.Context, color: discord.Colour):
        """
        View information and a preview of a color.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://www.thecolorapi.com/id?hex={str(color)[1:]}"
            ) as r:
                if r.status == 200:
                    data = await r.json()
                else:
                    await ctx.send(
                        "Something is wrong with the API I use, please try again later."
                    )
                    return

        embed = discord.Embed(color=color, title=data["name"]["value"])
        embed.set_thumbnail(
            url=f"https://api.alexflipnote.dev/color/image/{str(color)[1:]}"
        )
        embed.set_image(
            url=f"https://api.alexflipnote.dev/color/image/gradient/{str(color)[1:]}"
        )
        embed.description = (
            "```yaml\n"
            f"Hex: {color}\n"
            f"RGB: {data['rgb']['value']}\n"
            f"HSL: {data['hsl']['value']}\n"
            f"HSV: {data['hsv']['value']}\n"
            f"CMYK: {data['cmyk']['value']}\n"
            f"XYZ: {data['XYZ']['value']}"
            "```"
        )
        await ctx.send(embed=embed)

async def setup(bot):
    bot.add_cog(Color(bot))