
import discord
from redbot.core import commands, Config
import re
from typing import Optional

class Screenshot(commands.Cog):
    """Sends screenshot from websites."""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=69696969696)
        self.config.register_global(screenshot_key=True)

    @commands.group(invoke_without_command=True, aliases=['ss'])
    async def screenshot(self, ctx: commands.Context, site: str, device: str = 'desktop', delay: int = 0):
        """Get screenshot from a website."""
        URL_REGEX = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
        if not re.fullmatch(URL_REGEX, site):
            return await ctx.send('Invalid URL.')
        if not device.lower() in ['phone', 'desktop', 'tablet']:
            return await ctx.send('Valid devices are: phone, desktop and tablet.')
        if delay < 0:
            delay = 0
        if delay >= 30:
            delay = 30
        key = await self.config.screenshot_key()
        if key is None:
            return await ctx.send(f'Ask the bot owner to set an api key for https://api.screenshotmachine.com using `{ctx.clean_prefix}screenshot setkey <key>`')
        ScreenShot = f'https://api.screenshotmachine.com/?key={key}&url={site}&dimension=fullxfull&device={device}&delay={str(delay)}'
        embed = discord.Embed(color=await ctx.embed_color())
        embed.title = site
        embed.url = site
        embed.set_image(url=ScreenShot)
        try:
            await ctx.author.send(embed=embed)
            await ctx.send('Screenshot sent directly.')
        except:
            await ctx.send('Failed to send screenshot, make sure to have dms open.')

    @screenshot.command(name='setkey')
    @commands.is_owner()
    async def screenshot_setkey(self, ctx, key: str):
        """Sets an API key."""
        await self.config.screenshot_key.set(key)
        await ctx.send('Successfully set new API key.')

async def setup(bot):
    bot.add_cog(Screenshot(bot))