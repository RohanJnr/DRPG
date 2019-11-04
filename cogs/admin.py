import logging

from utils.database import db_functions as db
from utils.checks import is_admin

from discord.ext.commands import Bot, Cog, command


log = logging.getLogger('bot.' + __name__)


class AdminCog(Cog, name='Admin'):
    """Admin commands"""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.config = self.bot.config

    @is_admin()
    @command(name="hardreset", hidden=True)
    async def hard_reset(self, ctx):
        db_connection = await db.dbconnection()
        cursor = await db_connection.cursor()
        sql = "DELETE FROM `character` WHERE 1 = 1"
        await cursor.execute(sql)
        await db_connection.commit()
        await cursor.close()
        db_connection.close()
        return await ctx.send("Database Cleared.")


def setup(bot):
    bot.add_cog(AdminCog(bot))
    log.debug('Loaded')
