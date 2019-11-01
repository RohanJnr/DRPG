import asyncio
import logging

from utils.db_connection import dbconnection
from utils.functions_ import is_empty

from discord import Embed, Colour
from discord.ext.commands import Cog, command


log = logging.getLogger('bot.' + __name__)


class CharCog(Cog, name='Character Commands'):
    """Commands relating your character"""

    def __init__(self, bot):
        self.bot = bot

    @command(name="character")
    async def character_cmd(self, ctx):
        """View your character or create one."""
        db_connection = await dbconnection()
        cursor = await db_connection.cursor()
        user_id = ctx.author.id
        channel = ctx.channel
        select_characters = "SELECT * FROM `character` WHERE user_id = '%s'"
        val = user_id
        await cursor.execute(select_characters, (val,))
        result = await cursor.fetchall()
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
            # insert the data the user has submitted
            sql = "INSERT INTO `character`(`name`, user_id, description) VALUES(%s, %s, %s)"
            val = (character_name, user_id, character_description)
            await cursor.execute(sql, val)
            # insert the standard data that is set on default
            sql = "INSERT INTO inventory(character_id, gold) VALUES(%s, %s)"
            val = (user_id, 100)
            await cursor.execute(sql, val)
            sql = "INSERT INTO jobs(character_id, job) VALUES(%s, %s)"
            val = (user_id, 'miner')
            await cursor.execute(sql, val)
            try:
                await db_connection.commit()
                await cursor.close()
                db_connection.close()
                return await ctx.send('Succesfully created your character! Use !character to acces it.')
            except:
                await cursor.close()
                db_connection.close()
                return await ctx.send('Could not create your character. Something went wrong.')
        else:
            select_character = "SELECT `name`, description, gold FROM `character` " \
                               "LEFT JOIN inventory ON `character`.user_id = inventory.character_id " \
                               "WHERE `character`.user_id = '%s'"
            val = user_id
            await cursor.execute(select_character, (val,))
            results = await cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            result = []
            for row in results:
                row = dict(zip(columns, row))
                result.append(row)
            embed = Embed(title=result[0]['name'], colour=Colour.blurple(), description=result[0]['description'])
            embed.add_field(name='Inventory', value=f"**Gold:** {result[0]['gold']}", inline=False)
            await cursor.close()
            db_connection.close()
            return await ctx.send(embed=embed)

    @command(name="reset")
    async def reset_cmd(self, ctx):
        """Reset your character."""
        db_connection = await dbconnection()
        cursor = await db_connection.cursor()
        user_id = ctx.author.id
        channel = ctx.channel
        select_characters = "SELECT * FROM `character` WHERE user_id = '%s'"
        val = user_id
        await cursor.execute(select_characters, (val,))
        result = await cursor.fetchall()
        if is_empty(result) is True:
            await cursor.close()
            db_connection.close()
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
                    await cursor.execute(sql, (val,))
                    try:
                        await db_connection.commit()
                        await cursor.close()
                        db_connection.close()
                        return await ctx.send('Character removed. Use !character to create a new one.')
                    except:
                        await cursor.close()
                        db_connection.close()
                        return await ctx.send('Could not remove your character. Something went wrong.')
                elif msg.content == 'n' or msg.content == 'N':
                    await cursor.close()
                    db_connection.close()
                    return await ctx.send("Character reset cancelled.")
            except asyncio.TimeoutError:
                await ctx.send('No response. Character reset stopped.')
                await cursor.close()
                db_connection.close()


def setup(bot):
    bot.add_cog(CharCog(bot))
    log.debug('Loaded')
