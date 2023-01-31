import asyncio
import copy
import discord
import re

from redbot.core import Config, commands, checks


EMOJI_RE = re.compile("(<a?)?:\\w+:(\\d{18,19}>)?")
EMOJI_ID_RE = re.compile("\\d{18,19}")


class SmartReact(commands.Cog):
    """Create automatic reactions when trigger words are typed in chat."""

    default_guild_settings = {"reactions": {}}

    def __init__(self, bot):
        self.bot = bot
        self.conf = Config.get_conf(self, identifier=964952632)
        self.conf.register_guild(**self.default_guild_settings)

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    @checks.mod_or_permissions(administrator=True)
    @commands.bot_has_permissions(add_reactions=True, read_message_history=True)
    @commands.guild_only()
    @commands.command()
    async def addreact(self, ctx, member: discord.Member, emoji):
        """
        Add an auto reaction to a member.
        The `emoji` can be either the emoji itself, or in the case of a custom emoji, the ID.
        """
        emoji = self.fix_custom_emoji(emoji)
        await self.create_smart_reaction(ctx.guild, member, emoji, ctx.message)

    @checks.mod_or_permissions(administrator=True)
    @commands.bot_has_permissions(add_reactions=True, read_message_history=True)
    @commands.guild_only()
    @commands.command()
    async def removereact(self, ctx, member: discord.Member, emoji):
        """
        Delete an auto reaction to a member.
        The `emoji` can be either the emoji itself, or in the case of a custom emoji, the ID.
        """
        emoji = self.fix_custom_emoji(emoji)
        await self.remove_smart_reaction(ctx.guild, member, emoji, ctx.message)


    def fix_custom_emoji(self, emoji):
        # custom emoji id
        if re.match(EMOJI_ID_RE, emoji):
            e = self.bot.get_emoji(int(emoji))
            if e:
                return e

        # default emoji
        custom_emoji_match = EMOJI_RE.search(emoji)
        if not custom_emoji_match:
            return emoji

        # animated or static custom emoji
        e = emoji.split(":")[2][:-1].strip()
        try:
            e = self.bot.get_emoji(int(e))
        except ValueError:
            return None
        if e:
            return e

        # or, nothing matched
        return None

    async def create_smart_reaction(self, guild, member, emoji, message):
        try:
            # Use the reaction to see if it's valid
            await message.add_reaction(emoji)
            emoji = str(emoji)
            reactions = await self.conf.guild(guild).reactions()
            if emoji in reactions:
                if member.id in reactions[emoji]:
                    await message.channel.send("This smart reaction already exists.")
                    return
                reactions[emoji].append(member.id)
            else:
                reactions[emoji] = [member.id]
            await self.conf.guild(guild).reactions.set(reactions)
            await message.channel.send("Successfully added this reaction.")

        except (discord.errors.HTTPException, discord.errors.InvalidArgument):
            await message.channel.send("That's not an emoji I recognize. " "(might be custom!)")

    async def remove_smart_reaction(self, guild, member, emoji, message):
        try:
            # Use the reaction to see if it's valid
            await message.add_reaction(emoji)
            emoji = str(emoji)
            reactions = await self.conf.guild(guild).reactions()
            if emoji in reactions:
                if member.id in reactions[emoji]:
                    reactions[emoji].remove(member.id)
                    await self.conf.guild(guild).reactions.set(reactions)
                    await message.channel.send("Removed this smart reaction.")
                else:
                    await message.channel.send("That emoji is not used as a reaction for that word.")
            else:
                await message.channel.send("There are no smart reactions which use this emoji.")
        except (discord.errors.HTTPException, discord.errors.InvalidArgument):
            await message.channel.send("That's not an emoji I recognize. (might be custom!)")

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
            return
        if not message.channel.permissions_for(message.guild.me).add_reactions:
            return
        if message.author.id == self.bot.user.id:
            return
        reacts = copy.deepcopy(await self.conf.guild(message.guild).reactions())
        if reacts is None:
            return
        for emoji in reacts:
            for memberID in reacts[emoji]:
                if memberID in message.content:
                    emoji = self.fix_custom_emoji(emoji)
                    if not emoji:
                        return
                    try:
                        await message.add_reaction(emoji)
                    except (discord.errors.Forbidden, discord.errors.InvalidArgument, discord.errors.NotFound):
                        pass
                    except discord.errors.HTTPException:
                        if emoji in reacts:
                            del reacts[emoji]
                            await self.conf.guild(message.guild).reactions.set(reacts)


def setup(bot) -> None:
    bot.add_cog(SmartReact(bot))