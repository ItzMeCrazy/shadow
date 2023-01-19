
from typing import Optional
import discord
from redbot.core import commands

class Device(commands.Cog):
    """Tells the device the user is using."""

    __version__ = "1.0.0"

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def device(self, ctx: commands.Context, user: Optional[discord.Member] = None) -> None:
        """Displays the device user is using."""
        user = user if user else ctx.author
        devices = []
        if user.web_status in [discord.Status.online, discord.Status.idle, discord.Status.dnd]:
            devices.append("A Web 💻 device")
        if user.desktop_status in [discord.Status.online, discord.Status.idle, discord.Status.dnd]:
            devices.append("A Desktop 🖥️ device")
        if user.mobile_status in [discord.Status.online, discord.Status.idle, discord.Status.dnd]:
            devices.append("A Mobile 📱 device")
        if len(devices) == 0:
            await ctx.send(embed=discord.Embed(title=f"{user.name} is offline on all devices.", color=0xFF0000))
            return
        deviceString = ""
        if len(devices) > 1:
            deviceString =  ', '.join(devices[:-1]) + ' and ' + devices[-1]
        else:
            deviceString = devices[0]
        if len(devices) > 1:
            devices[-1] = "and " + devices[-1]
        deviceString = ', '.join(devices)
        embed = discord.Embed(title=f"{user.name} is using {deviceString}.", color=0x00ff00)
        await ctx.send(embed=embed)

async def setup(bot):
    bot.add_cog(Device(bot))