import logging
import yaml
import mysql.connector
import asyncio

from utils.functions_ import is_empty
from pathlib import Path

from discord.ext.commands import Cog, command
from discord import Embed, Colour

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
        """View your character."""
        user_id = ctx.author.id
        channel = ctx.channel
        select_characters = "SELECT * FROM `character` WHERE user_id = '%s'"
        val = user_id
        cursor.execute(select_characters, (val,))
        result = cursor.fetchall()
        if is_empty(result) is True:
            await ctx.send("Starting character creation process, what do you want your character to be called?")
            try:
                def check(m):
                    return m.channel == channel and ctx.author == m.author
                msg = await self.bot.wait_for('message', timeout=15.0, check=check)
            except asyncio.TimeoutError:
                return await ctx.send('No response. Character creation stopped.')
            character_name = msg.content
            await ctx.send('Give me a short background on your character.')
            try:
                def check(m):
                    return m.channel == channel and ctx.author == m.author
                msg = await self.bot.wait_for('message', timeout=120.0, check=check)
            except asyncio.TimeoutError:
                return await ctx.send('No response. Character creation stopped.')
            character_description = msg.content
            sql = "INSERT INTO `character`(`name`, user_id, description) VALUES(%s, %s, %s)"
            val = (character_name, user_id, character_description)
            cursor.execute(sql, val)
            try:
                db_connection.commit()
                return await ctx.send('Succesfully created your character! Use !character to acces it.')
            except:
                return await ctx.send('Could not create your character. Something went wrong.')
        else:
            select_character = "SELECT `name`, description FROM `character` WHERE user_id = '%s'"
            val = user_id
            cursor.execute(select_character, (val,))
            result = cursor.fetchall()
            results = dict(zip(cursor.column_names, result[0]))
            embed = Embed(title=results['name'], colour=Colour.blurple(), description=results['description'])
            return await ctx.send(embed=embed)

    @command(name="reset")
    async def reset_cmd(self, ctx):
        """Reset your character."""
        user_id = ctx.author.id
        channel = ctx.channel
        select_characters = "SELECT * FROM `character` WHERE user_id = '%s'"
        val = user_id
        cursor.execute(select_characters, (val,))
        result = cursor.fetchall()
        if is_empty(result) is True:
            return await ctx.send("Can't reset progress because you havent created a character yet.")
        else:
            await ctx.send("Are you sure you want to reset your progress? y/n")
            try:
                def check(m):
                    return m.channel == channel and ctx.author == m.author
                msg = await self.bot.wait_for('message', timeout=15.0, check=check)
                if msg.content == 'y' or msg.content == 'Y':
                    sql = "DELETE FROM `character` WHERE user_id = '%s'"
                    val = user_id
                    cursor.execute(sql, (val,))
                    try:
                        db_connection.commit()
                        return await ctx.send('Character removed. Use !character to create a new one.')
                    except:
                        return await ctx.send('Could not remove your character. Something went wrong.')
                elif msg.content == 'n' or msg.content == 'N':
                    return await ctx.send("Character reset cancelled.")
            except asyncio.TimeoutError:
                await ctx.send('No response. Character reset stopped.')


def setup(bot):
    bot.add_cog(CharCog(bot))
    log.debug('Loaded')
