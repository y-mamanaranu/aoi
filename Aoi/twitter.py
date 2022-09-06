import jinja2
from discord import app_commands
from discord.app_commands import locale_str as _T
from discord.ext import commands
from discord.ext import tasks
from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
import discord
import io
import tweepy
import asyncio
import unicodedata

from . import (
    get_database_url,
    help_command,
    get_twitter_consumer_key,
    get_twitter_consumer_secret,
)
from .database import (
    get_tt_tat_tats,
    update_twitter_template,
)

DATABASE_URL = get_database_url()
CONSUMER_KEY = get_twitter_consumer_key()
CONSUMER_SECRET = get_twitter_consumer_secret()


def get_east_asian_width_count(text):
    count = 0
    for c in text:
        v = unicodedata.east_asian_width(c)
        if v in 'FWA':
            count += 2
        else:
            count += 1
    return count


def create_message(template):
    jT = jinja2.Template(template)
    return jT.render()


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
        GUILD_ID = interaction.guild_id

        template, access_token, access_token_secret = get_tt_tat_tats(DATABASE_URL,
                                                                      GUILD_ID)

        if None in [access_token, access_token_secret]:
            await interaction.response.send_message("Need authorize twitter.")
            return
        if template is None:
            await interaction.response.send_message("Need template set.")
            return
        else:
            await interaction.response.defer()

        msg = create_message(template)
        while get_east_asian_width_count(msg) > 278:
            msg = create_message(template)

        client = tweepy.Client(consumer_key=CONSUMER_KEY,
                               consumer_secret=CONSUMER_SECRET,
                               access_token=access_token,
                               access_token_secret=access_token_secret)
        res = client.create_tweet(text=msg)

        URL = f"https://twitter.com/i/web/status/{res.data['id']}"

        await interaction.followup.send(f'ツイートしました。\n{URL}')

    @app_commands.command()
    @help_command()
    async def settwitter(self, interaction: discord.Interaction, clear: bool = False, help: bool = False):
        """Change template for tweet.

        Previlage of administrator is required.

        > /settwitter
        > <Template of tweet passed to jinja2.Template>

        Parameters
        ----------
        interaction : discord.Interaction
            _description_
        clear : str, by default False
            Wether to clear template.
        help : bool, optional
            _description_, by default False
        """
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Previlage of administrator is required.")
            return

        GUILD_ID = interaction.guild_id

        if clear:
            template = None

            update_twitter_template(DATABASE_URL, GUILD_ID, template)
            await interaction.response.send_message("twitter_template is changed "
                                                    f"to {template}.")
        else:
            await interaction.response.send_message("Input template as jinja2.Template.")

            def check(m):
                """Check if it's the same user and channel."""
                return m.author == interaction.user and m.channel == interaction.channel

            try:
                response = await self.bot.wait_for('message', check=check, timeout=30.0)
            except asyncio.TimeoutError:
                await interaction.followup.send("settwitter is canceled with timeout.")
                return
            template = response.content

            update_twitter_template(DATABASE_URL, GUILD_ID, template)
            await interaction.followup.send("twitter_template is changed "
                                            f"to following:\n{template}.")
        return

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

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        redirect_url = auth.get_authorization_url()
        await interaction.response.send_message(f"On develop.\n{redirect_url}")


async def setup(bot):
    await bot.add_cog(Twitter(bot))
