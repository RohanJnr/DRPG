import logging

from utils.functions_ import is_empty
from utils.db_connection import dbconnection

from discord import Colour, Embed
from discord.ext.commands import Bot, Cog
from discord.ext import commands

log = logging.getLogger('bot.' + __name__)


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


def setup(bot):
    bot.add_cog(JobsCog(bot))
    log.debug('Loaded')
