

from datetime import datetime
import discord
from redbot.core import commands
from discord_components import DiscordComponents, Button




class Sugari(commands.Cog):
    """Sugari bot support."""

    __version__ = "1.0.0"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['s', 'sup'])
    @commands.has_permissions(manage_messages=True)
    async def support(self, ctx: commands.Context):
        """Send sugari bot support embed."""
        await ctx.message.delete()
        embed = discord.Embed(color=0x2f3136)
        embed.set_author(name='Sugari Bot Support', icon_url='https://images-ext-1.discordapp.net/external/F8iaMFs9EJf3acEXHpOKu_QbaueI3W5P4OqPzMNIsu8/https/cdn.discordapp.com/emojis/806329146648166420.png')
        embed.title = 'Support'
        embed.set_thumbnail(url='https://images-ext-2.discordapp.net/external/R6q70bpCJCX6ji_vUCn9aOZGytbsDknZdWYDPExTIN8/https/cdn.discordapp.com/emojis/845736635442266132.png'
        )
        embed.description = '> Before asking anything, read <#1011547489096179722>.\n\n> Make sure to add a screenshot of your problem and describe it completely so that support staff can quickly assist you.\n> Before asking, scroll up a bit in support channel to check if same question was answered recently.\n\n> Ask questions related to Sugari only, asking questions for other bots will result in a timeout.\n\n> To report bugs, make sure you can reproduce the bug multiple times and make sure to attach a screenshot and explain how the bug was triggered.\n\n> Do not chat or send any off-topic messages here.\n\n*Wait for 30 minutes before pinging a staff member, If no one answered in 30 minutes you can ping any online staff member.*'
        embed.set_footer(text='Make sure to leave a review at voting websites.', icon_url='https://images-ext-1.discordapp.net/external/JEsa8Xu4EY4Z8955BYi-o5nEuimEsMOZ3V1z8bpivV0/https/cdn.discordapp.com/emojis/961062536390770690.gif')
        invite_emoji = discord.utils.get(self.bot.emojis, id=981441189460975646)
        action_row = [ Button(label='Invite Sugari', style=5, url='https://canary.discord.com/api/oauth2/authorize?client_id=981225490012602378&permissions=138012904772&scope=applications.commands%20bot', emoji=invite_emoji) ]
        await ctx.send(embed=embed, components=action_row)

async def setup(bot):
    DiscordComponents(bot)
    bot.add_cog(Sugari(bot))