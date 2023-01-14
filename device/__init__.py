
import discord
from redbot.core import commands

class Device(commands.Cog):
    """Tells the device the user is using."""

    __version__ = "1.0.0"

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def device(self, ctx: commands.Context, user: discord.Member) -> None:
        """Displays the device user is using."""
        if user.web_status in [discord.Status.online, discord.Status.idle, discord.Status.dnd]:
            device = "Web 💻"
        elif user.desktop_status in [discord.Status.online, discord.Status.idle, discord.Status.dnd]:
            device = "Desktop 🖥️"
        elif user.mobile_status in [discord.Status.online, discord.Status.idle, discord.Status.dnd]:
            device = "Mobile 📱"
        else:
            await ctx.send(f"{user.name} is offline on all devices.")
            return
        embed = discord.Embed(title=f"{user.name} is using a {device} device.", color=0x00ff00)
        await ctx.send(embed=embed)

async def setup(bot):
    bot.add_cog(Device(bot))