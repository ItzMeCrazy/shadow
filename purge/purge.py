from typing import Optional
import discord
from redbot.core import commands, checks


class Purge(commands.Cog):
    """Moderation purge command."""

    __version__ = "1.0.0"

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(manage_messages=True)
    @checks.admin_or_permissions(manage_messages=True)
    async def purge(
        self, ctx: commands.Context, limit: int, member: Optional[discord.Member]
    ) -> None:
        """Purge messages in a given channel."""
        if limit > 1000:
            await ctx.send("Cannot purge more than 1000 messages")
            return
        if member:

            def is_member(m):
                return m.author == member

            deleted = await ctx.channel.purge(limit=limit, check=is_member)

        else:
            deleted = await ctx.channel.purge(limit=limit)
        await ctx.send(f"Deleted {len(deleted)} message(s)", delete_after=5)
