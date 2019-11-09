import asyncio
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path

import discord
from discord.ext import commands

from utils.database.db_functions import CHARACTER_DATA
from utils.database import db_functions as db

logger = logging.getLogger(f"bot.{__name__}")


class DailyRewords(commands.Cog):
	"""A cog for giving away daily rewords."""

	def __init__(self, bot):
		self.bot = bot
		self.json_data = self.get_json()

	def get_json(self):
		p = Path("jsons", "rewords.json")
		with p.open() as file:
			info = json.load(file)
			return info


	async def background_loop(self):
		tomorrow = datetime.now() + timedelta(1)
		midnight = datetime(
			year=tomorrow.year,
			month=tomorrow.month,
			day=tomorrow.day,
			hour=0,
			minute=0,
			second=0
			)
		seconds_left = (midnight-datetime.now()).seconds
		await asyncio.sleep(10)
		while True:
			for character in CHARACTER_DATA:
				discord_id = character['owner']
				user = self.bot.get_user(discord_id)
				await self.give_reword(user)

			await asyncio.sleep(24*60*60)

	async def give_reword(self, user):
		weekday = datetime.today().weekday()
		rewords = self.json_data[str(weekday)]  # whatever reword
		sql = "select * from `character` where user_id=%s"
		values = (user.id, )
		result = await db.sql_query(sql, values)
		result = result[0]
		# add reword gold to existing gold and update value in table


def setup(bot):
	loop = asyncio.get_event_loop()
	loop.create_task(DailyRewords(bot).background_loop())
	bot.add_cog(DailyRewords(bot))
	logger.debug("Loaded")
