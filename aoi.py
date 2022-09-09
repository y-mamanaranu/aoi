import asyncio
import discord
from discord.ext import commands
from Aoi import (
    get_token,
    get_database_url,
    get_delta
)
from Aoi.database import (
    init_db,
    get_prefix,
    remove_ids,
    insert_ids,
)
from Aoi.translator import Translator
from logging import getLogger, INFO, StreamHandler
# from logging import DEBUG

# Setup logging
logger_level = INFO
# logger_level = DEBUG
logger = getLogger(__name__)
logger.setLevel(logger_level)

ch = StreamHandler()
ch.setLevel(logger_level)
logger.addHandler(ch)

# Get envriomental variables.
TOKEN = get_token()
DATABASE_URL = get_database_url()

# Initialize Heroku Postgres
init_db(DATABASE_URL)


def get_prefix_ctx(client, message):
    """Get prefix in context."""
    GUILD_ID = message.guild.id
    PREFIX = get_prefix(DATABASE_URL, GUILD_ID)
    return PREFIX


class Bot(commands.Bot):
    def __init__(self, command_prefix, *, help_command=None,
                 intents: discord.Intents):
        super().__init__(command_prefix=command_prefix,
                         help_command=help_command,
                         intents=intents)

    async def setup_hook(self):
        await self.tree.set_translator(Translator())
        await self.tree.sync()
        # await self.change_presence(activity=discord.Game(name=";help"))


intents = discord.Intents.all()
intents.reactions = True
intents.members = True
intents.messages = True
bot = Bot(command_prefix=(get_prefix_ctx),
          intents=intents)

asyncio.run(bot.load_extension("Aoi.profiles"))
asyncio.run(bot.load_extension("Aoi.movers"))
asyncio.run(bot.load_extension("Aoi.tenki_jp"))
asyncio.run(bot.load_extension("Aoi.twitter"))
asyncio.run(bot.load_extension("Aoi.setter"))


@bot.event
async def on_ready():
    delta = get_delta()
    loop = asyncio.get_running_loop()
    loop.call_later(delta, bot.cogs["Tenki_JP"].post_tenki.start)


@bot.event
async def on_guild_join(guild):
    """When the bot joins the guild."""
    insert_ids(DATABASE_URL, guild.id)


@bot.event
async def on_guild_remove(guild):
    """When the bot is removed from the guild."""
    remove_ids(DATABASE_URL, guild.id)

bot.run(TOKEN)
