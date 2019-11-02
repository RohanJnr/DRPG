from utils.database.db_functions import GUILD_SETTINGS


def is_empty(structure):
    if structure:
        # structure is not empty return false
        return False
    else:
        # structure is empty return true
        return True

def get_prefix(bot, message):
	if not message.guild:
		return bot.config["prefix"]
	try:
		prefix = GUILD_SETTINGS[message.guild.id]
	except KeyError:
		prefix = bot.config["prefix"]

	return prefix
