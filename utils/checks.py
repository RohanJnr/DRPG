from discord.ext.commands import check


bot_admin = 391583287652515841


def is_admin():
    def predicate(ctx):
        if ctx.author.id != bot_admin:
            return False
        return True
    return check(predicate)