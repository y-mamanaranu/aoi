from discord import app_commands
from discord.app_commands import locale_str as _T
from discord.ext import commands
from discord.ext import tasks
from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
import discord
import io

from . import (
    convert_channel_to_mention,
    get_database_url,
    help_command,
    get_twitter_consumer_key,
    get_twitter_consumer_secret,
)
from .database import (
    get_all_tenki_id,
    update_tenki_id,
    # get_twitter_template,
    # get_twitter_access_token,
    # get_twitter_access_token_secret,
    # update_twitter_template,
)

DATABASE_URL = get_database_url()
CONSUMER_KEY = get_twitter_consumer_key()
GET_TWITTER_CONSUMER_SECRET = get_twitter_consumer_secret()


class Twitter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @help_command()
    async def tweet(self, interaction: discord.Interaction, help: bool = False):
        """Tweet.

        Need authorize and set template of twitter.

        Parameters
        ----------
        interaction : discord.Interaction
            _description_
        help : bool, optional
            _description_, by default False
        """
        pass

    @app_commands.command()
    @help_command()
    async def settwitter(self, interaction: discord.Interaction, template: str, help: bool = False):
        """Change template for tweet.

        Previlage of administrator is required.

        Parameters
        ----------
        interaction : discord.Interaction
            _description_
        template : str
            Template of tweet passed to jinja2.Template
        help : bool, optional
            _description_, by default False
        """
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Previlage of administrator is required.")
            return

        pass

    @app_commands.command()
    @help_command()
    async def authtwitter(self,
                          interaction: discord.Interaction,
                          clear: bool = False,
                          help: bool = False):
        """Authorize twitter account.

        Previlage of administrator is required.

        Parameters
        ----------
        interaction : discord.Interaction
            _description_
        clear : str
            Wether to clear auth instead
        help : bool, optional
            _description_, by default False
        """
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Previlage of administrator is required.")
            return

        pass


async def setup(bot):
    await bot.add_cog(Twitter(bot))
