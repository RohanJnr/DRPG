import datetime
import logging
import yaml

from pathlib import Path

from discord import __version__ as discver, Activity, ActivityType
from discord.ext.commands import Bot


CONFIG_FILE = Path('config.yaml')
LOGDIR = Path('logs')


# Set up logging
def setup_logger() -> logging.Logger:
    """Create and return the root Logger object for the bot."""
    LOGDIR.mkdir(exist_ok=True)
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    logfile = LOGDIR / f'{timestamp}.log'
    logger = logging.getLogger('bot')  # the actual logger instance
    logger.setLevel(logging.DEBUG)  # capture all log levels
    console_log = logging.StreamHandler()
    console_log.setLevel(logging.DEBUG)  # log levels to be shown at the console
    file_log = logging.FileHandler(logfile)
    file_log.setLevel(logging.DEBUG)  # log levels to be written to file
    formatter = logging.Formatter('{asctime} - {name} - {levelname} - {message}', style='{')
    console_log.setFormatter(formatter)
    file_log.setFormatter(formatter)
    logger.addHandler(console_log)
    logger.addHandler(file_log)
    # additionally, do some of the same configuration for the discord.py logger
    discord_logger = logging.getLogger('discord')  # the discord.py logging instance
    discord_logger.setLevel(logging.INFO)  # DEBUG has far too much info
    discord_logger.addHandler(console_log)
    discord_logger.addHandler(file_log)
    return logger


log = setup_logger()

# Load configuration
with open(CONFIG_FILE, 'r') as yaml_file:
    config = yaml.safe_load(yaml_file)

bot = Bot(
    activity=Activity(
        name=f'{config["prefix"]}help',
        type=ActivityType.watching
    ),
    command_prefix="!",
    pm_help=True
)

bot.config = config  # assign configuration to a bot attribute for access from cogs
bot.remove_command('help')
bot.start_time = datetime.datetime.now()

@bot.event
async def on_ready():
    log.info(f"Connected as {bot.user}, using discord.py {discver}")


def main():
    """Load cogs, configuration, and start the bot."""
    for extension in bot.config['load_extensions']:
        try:
            log.debug(f'Loading extension: {extension}')
            bot.load_extension(extension)
        except:  # noqa: E722
            log.exception(f'Failed to load extension: {extension}')

    bot.run(config['token'])


if __name__ == '__main__':
    main()