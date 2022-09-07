from unicodedata import name
from discord import app_commands
from discord.app_commands import locale_str as _T
from discord.ext import commands
import discord
from emoji import demojize

from . import (
    get_database_url,
    has_permission,
    help_command,
)
from .database import (
    update_emoji_id,
    update_freshman_id,
    update_if_adjust,
    update_if_limit,
    update_log_id,
    update_prefix,
    update_profile_id,
    update_senior_id,
    update_if_create_text,
    update_if_create_voice,
    update_tenki_id,
    update_twitter_template,
    update_if_move,
)

DATABASE_URL = get_database_url()


class Setter(commands.GroupCog, name="set"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.describe(enable=_T('Wheter enable move commands.'))
    @help_command()
    @has_permission(move_members=True)
    async def move(self, interaction: discord.Integration, enable: bool, help: bool = False):
        """Change move?.

        Previlage to move members is required.

        Parameters
        ----------
        interaction : discord.Integration
            _description_
        enable : bool
            _description_
        help : bool, optional
            Wether to show help instead, by default False
        """
        GUILD_ID = interaction.guild_id

        update_if_move(DATABASE_URL, GUILD_ID, enable)
        await interaction.response.send_message(f"move? is changed to `{enable}`.")
        return

    @app_commands.command()
    @app_commands.describe(enable=_T('Wheter create text channel.'))
    @help_command()
    @has_permission(manage_channels=True)
    async def create_text(self, interaction: discord.Integration, enable: bool, help: bool = False):
        """Change create_text?.

        Previlage to manage channels is required.

        Parameters
        ----------
        interaction : discord.Integration
            _description_
        enable : bool
            _description_
        help : bool, optional
            Wether to show help instead, by default False
        """
        GUILD_ID = interaction.guild_id

        update_if_create_text(DATABASE_URL, GUILD_ID, enable)
        await interaction.response.send_message(f"create_text? is changed to `{enable}`.")
        return

    @app_commands.command()
    @app_commands.describe(enable=_T('Wheter create voice channel.'))
    @help_command()
    @has_permission(manage_channels=True)
    async def create_voice(self, interaction: discord.Integration, enable: bool, help: bool = False):
        """Change create_voice?.

        Previlage to manage channels is required.

        Parameters
        ----------
        interaction : discord.Integration
            _description_
        enable : bool
            _description_
        help : bool, optional
            Wether to show help instead, by default False
        """
        GUILD_ID = interaction.guild_id

        update_if_create_voice(DATABASE_URL, GUILD_ID, enable)
        await interaction.response.send_message(f"create_voice? is changed to `{enable}`.")
        return

    @app_commands.command()
    @app_commands.describe(enable=_T('Whether activate `/limit`.'))
    @help_command()
    @has_permission(manage_channels=True)
    async def limit(self, interaction: discord.Integration, enable: bool, help: bool = False):
        """Change limit?.

        Previlage to manage channels is required.

        Parameters
        ----------
        interaction : discord.Integration
            _description_
        enable : bool
            _description_
        help : bool, optional
            Wether to show help instead, by default False
        """
        GUILD_ID = interaction.guild_id

        update_if_limit(DATABASE_URL, GUILD_ID, enable)
        await interaction.response.send_message(f"limit? is changed to `{enable}`.")
        return

    @app_commands.command()
    @app_commands.describe(enable=_T('Wheter activate `on_voice_state_update`.'))
    @help_command()
    @has_permission(manage_channels=True)
    async def adjust(self, interaction: discord.Integration, enable: bool, help: bool = False):
        """Change adjust?.

        Previlage to manage channels is required.

        Parameters
        ----------
        interaction : discord.Integration
            _description_
        enable : bool
            _description_
        help : bool, optional
            Wether to show help instead, by default False
        """
        GUILD_ID = interaction.guild_id

        update_if_adjust(DATABASE_URL, GUILD_ID, enable)
        await interaction.response.send_message(f"adjust? is changed to `{enable}`.")
        return

    @app_commands.command()
    @app_commands.describe(prefix=_T('Prefix of command, Default prefix is `;`.'))
    @help_command()
    @has_permission(administrator=True)
    async def prefix(self, interaction: discord.Integration, prefix: str, help: bool = False):
        """Change prefix.

        Previlage of administrator is required.
        """
        GUILD_ID = interaction.guild_id

        prefix = str(prefix)
        update_prefix(DATABASE_URL, GUILD_ID, prefix)
        await interaction.response.send_message(f"Prefix is changed to `{prefix}`.")
        return

    @app_commands.command()
    @app_commands.describe(profile=_T('Profile channel, empty for disable.'))
    @help_command()
    @has_permission(administrator=True)
    async def profile(self, interaction: discord.Integration, profile: discord.TextChannel = None, help: bool = False):
        """Change #Profile.

        Previlage of administrator is required.
        """
        GUILD_ID = interaction.guild_id

        if profile is None:
            update_profile_id(DATABASE_URL, GUILD_ID, profile)
            await interaction.response.send_message("#Profile is changed "
                                                    f"to {profile}.")
        else:
            update_profile_id(DATABASE_URL, GUILD_ID, profile.id)
            await interaction.response.send_message("#Profile is changed "
                                                    f"to {profile.mention}.")
        return

    @app_commands.command()
    @app_commands.describe(log=_T('Log channel, empty for disable.'))
    @help_command()
    @has_permission(administrator=True)
    async def log(self, interaction: discord.Integration, log: discord.TextChannel = None, help: bool = False):
        """Change #Log.

        Previlage of administrator is required.
        """
        GUILD_ID = interaction.guild_id

        if log is None:
            update_log_id(DATABASE_URL, GUILD_ID, log)
            await interaction.response.send_message("#Log is changed "
                                                    f"to {log}.")
        else:
            update_log_id(DATABASE_URL, GUILD_ID, log.id)
            await interaction.response.send_message("#Log is changed "
                                                    f"to {log.mention}.")
        return

    @app_commands.command()
    @app_commands.describe(freshman=_T('Role to assign to new member, empty for disable.'))
    @help_command()
    @has_permission(manage_messages=True)
    async def freshman(self, interaction: discord.Integration, freshman: discord.Role = None, help: bool = False):
        """Change @Freshman.

        Previlage to manage roles is required.
        """
        GUILD_ID = interaction.guild_id

        if freshman is None:
            update_freshman_id(DATABASE_URL, GUILD_ID, freshman)
            await interaction.response.send_message("@Freshman is changed "
                                                    f"to {freshman}.")
        else:
            update_freshman_id(DATABASE_URL, GUILD_ID, freshman.id)
            await interaction.response.send_message("@Freshman is changed "
                                                    f"to {freshman.mention}.")
        return

    @app_commands.command()
    @app_commands.describe(
        senior=_T('Role who can assign to new member, empty for disable.'))
    @help_command()
    @has_permission(manage_messages=True)
    async def senior(self, interaction: discord.Integration, senior: discord.Role = None, help: bool = False):
        """Change @Senior.

        Previlage to manage roles is required.
        """
        GUILD_ID = interaction.guild_id

        if senior is None:
            update_senior_id(DATABASE_URL, GUILD_ID, senior)
            await interaction.response.send_message("@Senior is changed "
                                                    f"to {senior}.")
        else:
            update_senior_id(DATABASE_URL, GUILD_ID, senior.id)
            await interaction.response.send_message("@Senior is changed "
                                                    f"to {senior.mention}.")
        return

    @app_commands.command()
    @app_commands.describe(emoji=_T('Emoji to assign role, empty for matching all.'))
    @help_command()
    @has_permission(manage_roles=True)
    async def emoji(self, interaction: discord.Integration, emoji: str = None, help: bool = False):
        """Change :emoji:.

        Previlage of manage roles is required.
        """
        GUILD_ID = interaction.guild_id

        if emoji is None:
            update_emoji_id(DATABASE_URL, GUILD_ID, emoji)
            await interaction.response.send_message(":emoji: is changed "
                                                    f"to {emoji}.")
        else:
            emoji_id = demojize(emoji)
            update_emoji_id(DATABASE_URL, GUILD_ID, emoji_id)
            await interaction.response.send_message(":emoji: is changed "
                                                    f"to {emoji_id}.")
        return

    @app_commands.command()
    @app_commands.describe(tenki=_T('Weather forecast channel, empty for disable.'))
    @help_command()
    @has_permission(administrator=True)
    async def tenki(self,
                    interaction: discord.Interaction,
                    tenki: discord.TextChannel = None,
                    help: bool = False):
        """Change #Tenki.

        Previlage of administrator is required.

        Parameters
        ----------
        interaction : discord.Interaction
            _description_
        tenki : discord.TextChannel, optional
            Channel to set as #Tenki, by default None
            #Tenki is weather forecast channel.
            If #Tenki is not None, post wheter forecat of tenki.jp to #Tenki on 5:00 JST.
        help : bool, optional
            Wether to show help instead, by default False
        """
        GUILD_ID = interaction.guild_id

        if tenki is None:
            update_tenki_id(DATABASE_URL, GUILD_ID, tenki)
            await interaction.response.send_message("#Tenki is changed "
                                                    f"to {tenki}.")
        else:
            update_tenki_id(DATABASE_URL, GUILD_ID, tenki.id)
            await interaction.response.send_message("#Tenki is changed "
                                                    f"to {tenki.mention}.")
        return

    @app_commands.command()
    @help_command()
    @has_permission(administrator=True)
    async def twitter(self, interaction: discord.Interaction, clear: bool = False, help: bool = False):
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
        GUILD_ID = interaction.guild_id

        if clear:
            template = None

            update_twitter_template(DATABASE_URL, GUILD_ID, template)
            await interaction.response.send_message("twitter_template is changed "
                                                    f"to {template}.")
        else:
            class UI(discord.ui.Modal, title="twitter_template"):
                template = discord.ui.TextInput(
                    label='template',
                    style=discord.TextStyle.long,
                    placeholder='Input template as jinja2.Template.',
                )

                async def on_submit(self, interaction: discord.Interaction):
                    update_twitter_template(DATABASE_URL,
                                            GUILD_ID,
                                            self.template.value)
                    embed = discord.Embed(description=self.template.value)
                    await interaction.response.send_message("twitter_template is changed to following.",
                                                            embed=embed)

            await interaction.response.send_modal(UI())


async def setup(bot):
    await bot.add_cog(Setter(bot))
