import logging

from utils.functions_ import is_empty
from utils.database import db_functions as db

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
        db_connection = await db.dbconnection()
        cursor = await db_connection.cursor()
        user_id = ctx.author.id
        sql = "SELECT * FROM jobs WHERE character_id = '%s'"
        val = user_id
        await cursor.execute(sql, (val,))
        results = await cursor.fetchall()
        result = []
        available_jobs =[]
        columns = [desc[0] for desc in cursor.description]
        for row in results:
            row = dict(zip(columns, row))
            if row['current_job'] == 'false':
                result.append(row)
                available_jobs.append(row['job'])
        if is_empty(result):
            await cursor.close()
            db_connection.close()
            return await ctx.send("You may only have 1 job at a time.")
        else:
            if job_to_join in available_jobs:
                sql = "UPDATE jobs SET current_job = 'true' WHERE character_id = '%s' AND job = %s"
                val = (user_id, job_to_join.lower())
                await cursor.execute(sql, val)
                await db_connection.commit()
                await cursor.close()
                db_connection.close()
                return await ctx.send(f"Changed your job to: {job_to_join.lower()}.")
            else:
                await cursor.close()
                db_connection.close()
                return await ctx.send(f"That job doesnt exist. Pick one of the following: {[job for job in available_jobs]}")

    @job.command(name="leave")
    async def job_leave(self, ctx):
        """Leave your job."""
        db_connection = await db.dbconnection()
        cursor = await db_connection.cursor()
        user_id = ctx.author.id
        sql = "SELECT * FROM jobs WHERE character_id = '%s' AND current_job = %s"
        val = (user_id, 'true')
        await cursor.execute(sql, val)
        results = await cursor.fetchall()
        if is_empty(results):
            await cursor.close()
            db_connection.close()
            return await ctx.send("You dont have a job. Use `!job join {job_name}` to join one.")
        else:
            sql = "SELECT job FROM jobs WHERE current_job = %s"
            val = "true"
            await cursor.execute(sql, (val,))
            results = await cursor.fetchall()
            sql = "UPDATE jobs SET current_job = %s WHERE character_id = '%s' AND job = %s"
            val = ('false', user_id, results[0][0])
            await cursor.execute(sql, val)
            await db_connection.commit()
            await cursor.close()
            db_connection.close()
            return await ctx.send("Left your job.")


def setup(bot):
    bot.add_cog(JobsCog(bot))
    log.debug('Loaded')
