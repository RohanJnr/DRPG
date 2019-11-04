import logging

from discord.ext import commands

from utils.database import db_functions as db


logger = logging.getLogger(f"bot.{__name__}")


class Events(commands.Cog):
	"""A cog for managing events."""

	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		sql = "insert into guild_settings(guild_id, prefix) values(%s, %s)" 
		values = (guild.id, self.bot.config["prefix"])
		status = await db.sql_edit(sql, values)
		if status:
			logger.info(f"Guild {guild.id} has been added to the database.")
		else:
			logger.error(f"Guild {guild.id} could not be added to the database.")

	@commands.Cog.listener()
	async def on_guild_remove(self, guild):
		sql = "delete from guild_settings where guild_id = %s"
		values = (guild.id,)
		status = await db.sql_edit(sql, values)
		if status:
			logger.info(f"Guild {guild.id} has been removed from the database.")
		else:
			logger.error(f"Guild {guild.id} could not be removed from the database.")


def setup(bot):
	bot.add_cog(Events(bot))
	logger.info("loaded")