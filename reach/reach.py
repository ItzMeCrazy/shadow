from typing import Optional
import discord
from redbot.core import commands


class Reach(commands.Cog):
    """Shows the reach of roles in a channel"""

    __version__ = "1.0.0"

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reach(
        self,
        ctx: commands.Context,
        channel: discord.TextChannel,
        roles: commands.Greedy[discord.Role],
    ):
        """Shows the reach of roles in a channel"""
        members = 0
        total_members = 0
        for role in roles:
            total_members += len(role.members)
            for member in role.members:
                if channel.permissions_for(member).read_messages:
                    members += 1

        percent = 100 * members / total_members
        description = (
            f"Channel: {channel.mention} `{channel.id}`\n\n"
            + "\n".join(
                f"<:Arrow:1074035208640286810> {role.mention} `{role.id}` members: {len(role.members)} reach: {100 * len(role.members) / total_members:.2f}%"
                for role in roles
            )
            + f"\nTotal reach: {members} out of {total_members} targeted members\nwhich represents {percent:.2f}%"
        )

        embed = discord.Embed(
            title="**Roles Reach**", description=description, color=3092790
        )
        embed.set_footer(text="Run ';invite' to invite me!")
        await ctx.send(embed=embed)
