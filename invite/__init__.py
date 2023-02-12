from .invite import Invite


def setup(bot):
    _invite = bot.get_command("invite")
    if _invite:
        bot.remove_command(_invite.name)

    cog = Invite(bot)
    bot.add_cog(cog)
