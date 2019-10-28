import logging
import yaml
import mysql.connector

from utils.functions_ import is_empty
from pathlib import Path

from discord.ext.commands import Cog, command
from discord import Embed

log = logging.getLogger('bot.' + __name__)

NAMEFILE = Path('config.yaml')

with open(NAMEFILE, encoding='utf8') as f:
    data = yaml.safe_load(f)

db_connection = mysql.connector.connect(
    host=data['database']['host'],
    user=data['database']['user'],
    passwd=data['database']['passwd'],
    database=data['database']['database']
)

cursor = db_connection.cursor()


class CharCog(Cog, name='Character Commands'):
    """Commands relating your character"""

    def __init__(self, bot):
        self.bot = bot

    @command(name="character")
    async def test(self, ctx):
        """View your character sheet."""
        user_id = ctx.author.id
        sql = "SELECT * FROM `character` where id = 'user_id'"
        cursor.execute(sql)
        result = cursor.fetchall()
        if is_empty(result) is True:
            return await ctx.send("Je moet wel een character aanmaken")
        else:
            return await ctx.send("Je hebt inderdaad een character")


def setup(bot):
    bot.add_cog(CharCog(bot))
    log.debug('Loaded')
