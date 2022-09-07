import threading
from bottle import Bottle, ServerAdapter, request
import jinja2
from discord import app_commands
from discord.ext import commands
import discord
import os
import tweepy
import unicodedata
import time

from . import (
    get_database_url,
    help_command,
    get_twitter_consumer_key,
    get_twitter_consumer_secret,
    has_permission,
)
from .database import (
    get_tt_tat_tats,
    update_tat_tats,
)

DATABASE_URL = get_database_url()
CONSUMER_KEY = get_twitter_consumer_key()
CONSUMER_SECRET = get_twitter_consumer_secret()


class MyWSGIRefServer(ServerAdapter):
    server = None

    def run(self, handler):
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        if self.quiet:
            class QuietHandler(WSGIRequestHandler):
                def log_request(*args, **kw): pass
            self.options['handler_class'] = QuietHandler
        self.server = make_server(
            self.host, self.port, handler, **self.options)
        self.server.serve_forever()

    def stop(self):
        self.server.server_close()
        self.server.shutdown()


class AuthorizeApp():
    server = None
    app = None
    oauth_verifier = None

    def __init__(self, oauth_token):
        self.oauth_token = oauth_token

    def get_authorize(self):
        self.server = MyWSGIRefServer(port=int(os.environ.get("PORT", 5000)))
        self.app = Bottle()

        @self.app.route('/', method='GET')
        def authorize():
            oauth_token = request.query.get('oauth_token')
            oauth_verifier = request.query.get('oauth_verifier')

            if self.oauth_verifier or \
                    oauth_token != self.oauth_token or \
                    None in [oauth_token, oauth_verifier]:
                return 'Invalid Request'
            else:
                self.oauth_verifier = oauth_verifier
                return 'Authorized'

        self.app.run(server=self.server, reloder=False)


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
    @has_permission(administrator=True)
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
        GUILD_ID = interaction.guild_id

        if clear is True:
            update_tat_tats(DATABASE_URL,
                            GUILD_ID,
                            None,
                            None)
            await interaction.response.send_message("Clear Authorization.")
            return

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        redirect_url = auth.get_authorization_url()
        await interaction.response.send_message(redirect_url)

        print("Authorize server start.")
        oauth_token = auth.request_token["oauth_token"]
        app = AuthorizeApp(oauth_token)
        thread = threading.Thread(target=app.get_authorize)
        thread.start()
        criteria = time.time() + 30
        while not app.oauth_verifier and time.time() < criteria:
            pass
        app.server.stop()
        thread.join()
        print("Authorize server stop.")

        oauth_verifier = app.oauth_verifier

        if oauth_token is None:
            await interaction.followup.send("authtwitter is canceled with timeout.")
            return

        access_token, access_token_secret = auth.get_access_token(
            oauth_verifier)
        update_tat_tats(DATABASE_URL,
                        GUILD_ID,
                        access_token,
                        access_token_secret)

        await interaction.followup.send("Authorization success.")


async def setup(bot):
    await bot.add_cog(Twitter(bot))
