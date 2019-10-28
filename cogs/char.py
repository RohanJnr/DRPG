import logging
import yaml
import mysql.connector
import asyncio

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
    async def character_cmd(self, ctx):
        """View your character sheet."""
        user_id = ctx.author.id
        channel = ctx.channel
        select_characters = "SELECT * FROM `character` WHERE user_id = '%s'"
        val = user_id
        cursor.execute(select_characters, (val,))
        result = cursor.fetchall()
        if is_empty(result) is True:
            await ctx.send("Starting character creation process, what do you want your character to be called?")

            def check(m):
                return m.channel == channel and ctx.author == m.author

            try:
                msg = await self.bot.wait_for('message', timeout=15.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send('No response. Character creation stopped.')
            character_name = msg.content
            sql = "INSERT INTO `character`(`name`, user_id) VALUES(%s, %s)"
            val = (character_name, user_id)
            cursor.execute(sql, val)
            try:
                db_connection.commit()
                # printing what was inserted for debugging
                print(cursor.rowcount, "was inserted.")
                return await ctx.send('Succesfully created your character! Use !character to acces it.')
            except:
                return await ctx.send('Could not create your character. Something went wrong.')
        else:
            select_character = "SELECT `name` FROM `character` WHERE user_id = '%s'"
            val = user_id
            cursor.execute(select_character, (val,))
            result = cursor.fetchall()
            print(result)


def setup(bot):
    bot.add_cog(CharCog(bot))
    log.debug('Loaded')
