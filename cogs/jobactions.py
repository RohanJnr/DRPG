import logging
import random
import json

from utils.functions_ import has_job, dbconnection

from discord.ext.commands import Cog, command, cooldown
from discord.ext.commands.cooldowns import BucketType


log = logging.getLogger('bot.' + __name__)

with open('jsons/mining.json', 'r') as f:
    data = json.load(f)


class JobactionsCog(Cog, name='Job Actions'):
    """All possible actions with jobs."""

    def __init__(self, bot):
        self.bot = bot

    @command(name="mine")
    @cooldown(1, 60, BucketType.user)
    async def mine_cmd(self, ctx):
        """Miners can use this to mine ores."""
        db_connection = await dbconnection()
        cursor = await db_connection.cursor()
        user_id = ctx.author.id
        can_proceed = await has_job('miner', user_id)
        if can_proceed is True:
            sql = "SELECT `level`, actions FROM jobs WHERE character_id = '%s' AND job = %s"
            val = (user_id, 'miner')
            await cursor.execute(sql, val)
            results = await cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            result = []
            for row in results:
                row = dict(zip(columns, row))
                result.append(row)
            mining_level = result[0]['level']
            actions = result[0]['actions']
            for level in data:
                if actions >= level['actions_required']:
                    mining_level = level['level']
            for level in data:
                if level['level'] == mining_level:
                    ores = level['ores'][0]
            ore = random.choices(list(ores.keys()), weights=ores.values())[0]
            ore = ore.lower()
            sql = "UPDATE inventory SET " + ore + " = " + ore + "+ 1, skillshard = skillshard + 1 WHERE character_id " \
                                                                "= '%s' "
            val = user_id
            await cursor.execute(sql, (val,))
            await db_connection.commit()
            sql = "UPDATE jobs SET actions = actions + %s, `level` = %s WHERE character_id = '%s' AND job = %s"
            val = (1, mining_level, user_id, 'miner')
            await cursor.execute(sql, val)
            await db_connection.commit()
            await cursor.close()
            db_connection.close()
            return await ctx.send(f"You venture deep into the mines and find: {ore}. In addition you get 1 skill shard.")
        else:
            return await ctx.send("Only miners have acces to this command. To become one use: `!job join miner`")


def setup(bot):
    bot.add_cog(JobactionsCog(bot))
    log.debug('Loaded')
