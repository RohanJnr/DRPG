import logging

from utils.functions_ import is_empty
from utils.db_connection import dbconnection

from discord import Colour, Embed
from discord.ext.commands import Bot, Cog
from discord.ext import commands

log = logging.getLogger('bot.' + __name__)

db_connection = dbconnection()
cursor = db_connection.cursor()


class JobsCog(Cog, name='Jobs'):
    """Commands related to jobs."""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.config = self.bot.config

    @commands.group(name="job", invoke_without_command=True)
    async def job(self, ctx):
        """A tutorial on Jobs."""
        embed = Embed(title="Jobs", colour=Colour.blurple(), description=
                      """You can earn money by joining a job. 
                      To join a job use `!job join {job}` 
                      You can have 1 job at a time.
                      Each job has its own unique action, check the list below: 
                      **Miner:** `!mine`
                      """)
        return await ctx.send(embed=embed)

    @job.command(name="join")
    async def job_join(self, ctx, job_to_join: str):
        """Join a new job."""
        """
        user_id = ctx.author.id
        sql = "SELECT job FROM jobs WHERE character_id = '%s'"
        val = user_id
        cursor.execute(sql, (val,))
        result = cursor.fetchall()
        results = dict(zip(cursor.column_names, result[0]))
        if results['job'] == job_to_join or is_empty(result):
            await ctx.send("Joining your new job")
        else:
            return await ctx.send("You can only have 1 job at a time.")
        """


def setup(bot):
    bot.add_cog(JobsCog(bot))
    log.debug('Loaded')
