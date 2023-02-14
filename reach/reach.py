from typing import Optional, Union
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
        *roles: Union[discord.Role, str],
    ):
        """Shows the reach of roles in a channel"""
        if len(roles) == 0:
            await ctx.send("Please enter atleast one role to check reach of.")
            return
        members = set()
        total_members = set()
        description = f"Channel: {channel.mention} `{channel.id}`\n\n"
        for role in roles:
            if isinstance(role, str):
                if "everyone" in role.lower():
                    for member in ctx.guild.default_role.members:
                        total_members.add(member)
                        if channel.permissions_for(member).read_messages:
                            members.add(member)
                    description += f"\n<:Arrow:1074035208640286810> @everyone members: {len(ctx.guild.default_role.members)} reach: {100 * len(members) / len(ctx.guild.default_role.members):.2f}%"
                elif "@here" in role.lower():
                    for member in ctx.guild.members:
                        if member.status != discord.Status.offline:
                            total_members.add(member)
                            if channel.permissions_for(member).read_messages:
                                members.add(member)
                    description += f"\n<:Arrow:1074035208640286810> @here members: {len(total_members)} reach: {100 * len(members) / len(total_members):.2f}%"

                else:
                    await ctx.send("Invalid role passed.")
                    return
            else:
                for member in role.members:
                    total_members.add(member)
                    if channel.permissions_for(member).read_messages:
                        members.add(member)
                description += f"\n<:Arrow:1074035208640286810> {role.mention} `{role.id}` members: {len(role.members)} reach: {100 * len(role.members) / len(total_members):.2f}%"

        percent = 100 * len(members) / len(total_members)
        description += f"\nTotal reach: {len(members)} out of {len(total_members)} targeted members\nwhich represents {percent:.2f}%"

        embed = discord.Embed(
            title="**Roles Reach**", description=description, color=3092790
        )
        embed.set_footer(text="Run ';invite' to invite me!")
        await ctx.send(embed=embed)
