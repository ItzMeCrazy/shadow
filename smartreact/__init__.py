from .smartreact import SmartReact


def setup(bot) -> None:
    bot.add_cog(SmartReact(bot))
