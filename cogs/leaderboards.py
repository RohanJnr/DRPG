import logging

from utils.database import db_functions as db

from discord import Embed, Colour
from discord.ext.commands import Cog
from discord.ext import commands


log = logging.getLogger('bot.' + __name__)


class LeaderboardsCog(Cog, name='Leaderboards'):
    """Global leaderboards."""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="leaderboard", invoke_without_command=True)
    async def leaderboard(self, ctx):
        """A tutorial on Jobs."""
        embed = Embed(title="Leaderboards", colour=Colour.blurple(), description=
        """You can view all of the leaderboards with this commmand.
        The following leaderboards are available:
        `!leaderboard wealth` Shows the top 10 richest users.
        """)
        return await ctx.send(embed=embed)

    @leaderboard.command(name="wealth")
    async def top_wealth(self, ctx):
        """Shows the top 10 users with the most gold."""
        db_connection = await db.dbconnection()
        cursor = await db_connection.cursor()
        sql = "SELECT `character`.name, inventory.gold FROM inventory " \
              "JOIN `character` WHERE `character`.user_id = inventory.character_id " \
              "ORDER BY gold DESC LIMIT 10"
        await cursor.execute(sql)
        results = await cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        result = []
        for row in results:
            row = dict(zip(columns, row))
            result.append(row)
        desc = ""
        number = 0
        for entry in result:
            number += 1
            desc += f"**#{number}. {entry['name']}:** {entry['gold']} gold.\n"
        embed = Embed(title="Top 10 Wealth", colour=Colour.blurple(), description=desc)
        await cursor.close()
        db_connection.close()
        return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(LeaderboardsCog(bot))
    log.debug('Loaded')
