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
        if len(roles) == 0:
            await ctx.send("Please enter atleast one role to check reach of.")
            return
        members = set()
        total_members = set()
        for role in roles:
            for member in role.members:
                total_members.add(member)
                if channel.permissions_for(member).read_messages:
                    members.add(member)

        percent = 100 * len(members) / len(total_members)
        description = (
            f"Channel: {channel.mention} `{channel.id}`\n\n"
            + "\n".join(
                f"<:Arrow:1074035208640286810> {role.mention} `{role.id}` members: {len(role.members)} reach: {100 * len(role.members) / len(total_members):.2f}%"
                for role in roles
            )
            + f"\nTotal reach: {len(members)} out of {len(total_members)} targeted members\nwhich represents {percent:.2f}%"
        )

        embed = discord.Embed(
            title="**Roles Reach**", description=description, color=3092790
        )
        embed.set_footer(text="Run ';invite' to invite me!")
        await ctx.send(embed=embed)
