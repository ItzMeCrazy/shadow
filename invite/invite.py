import discord
from redbot.core import commands

_invite = None


class Invite(commands.Cog):
    """Invite bot to your server."""

    __version__ = "1.0.0"

    def __init__(self, bot):
        self.bot = bot

    def cog_unload(self):
        global _invite
        if _invite:
            try:
                self.bot.remove_command("invite")
            except:
                pass
            self.bot.add_command(_invite)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(2, 5, commands.BucketType.user)
    @commands.command()
    async def invite(self, ctx: commands.Context):
        """Invite the bot to your server."""
        embed = discord.Embed(color=await ctx.embed_color())
        url = f"https://discord.com/api/oauth2/authorize?client_id={ctx.bot.user.id}&permissions=8&scope=bot+applications.commands"
        embed.description = (
            f"Thanks for choosing to invite {ctx.bot.user.name} to your server."
        )
        embed.set_thumbnail(
            url=ctx.bot.user.avatar_url or ctx.bot.user.default_avatar_url
        )
        embed.set_author(name=ctx.bot.user.name, icon_url=ctx.bot.user.avatar_url)
        embed.set_footer(
            text=ctx.guild.name or "Thanks for inviting.",
            icon_url=ctx.guild.icon_url
            or ctx.bot.user.avatar_url
            or ctx.bot.user.default_avatar_url,
        )
        embed.add_field(name="Invite the bot.", value=f"[Click here to invite]({url})")
        await ctx.send(embed=embed)
