from os import link
from discord import app_commands
from discord.app_commands import locale_str as _T
from discord.ext import commands
from discord.utils import get
from emoji import demojize
import asyncio
import discord
import random
import re
import numpy as np

from . import (
    convert_channel_to_mention,
    convert_role_to_mention,
    get_database_url,
    help_command,
    has_permission,
)
from .database import (
    get_pre_pro_log_fre_sen_emo_ten_lim_adj_mov_icv_ict_tt,
    get_pro_log_fre_sen_emo,
    get_profile_id,
    get_twitter_status,
)

DATABASE_URL = get_database_url()


class Profiles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @help_command()
    async def detail(self, interaction: discord.Interaction, help: bool = False):
        """Show detail of parameters."""
        await interaction.response.send_message("""Prefix is Prefix of command.
#Profile is Profile channel.
#Log is Log channel.
@Freshman is Role to assign to new member.
@Senior is Role who can assign to new member.
:emoji: is Emoji to assign role.

#Tenki is weather forecast channel.

limit? is Whether activate `/limit`.
adjust? is Wheter activate `on_voice_state_update`.
move?.
create_voice?.
create_text?.

twitter account.
twitter template""")

    @app_commands.command()
    @help_command()
    async def status(self, interaction: discord.Interaction, help: bool = False):
        """Show current config."""
        GUILD_ID = interaction.guild_id

        PREFIX, \
            PROFILE_ID, \
            LOG_ID, \
            FRESHMAN_ID, \
            SENIOR_ID, \
            EMOJI_ID, \
            TENKI_ID, \
            IF_LIMIT, \
            IF_ADJUST, \
            IF_MOVE, \
            IF_CREATE_VOICE, \
            IF_CREATE_TEXT, \
            TEMPLATE = \
            get_pre_pro_log_fre_sen_emo_ten_lim_adj_mov_icv_ict_tt(DATABASE_URL,
                                                                   GUILD_ID)
        await interaction.response.defer()
        AUTH = get_twitter_status(DATABASE_URL, GUILD_ID)
        embed = discord.Embed(description=TEMPLATE)
        await interaction.followup.send(f"""Prefix is `{PREFIX}`.
#Profile is {convert_channel_to_mention(PROFILE_ID)}.
#Log is {convert_channel_to_mention(LOG_ID)}.
@Freshman is {convert_role_to_mention(FRESHMAN_ID)}.
@Senior is {convert_role_to_mention(SENIOR_ID)}.
:emoji: is {EMOJI_ID}.

#Tenki is {convert_channel_to_mention(TENKI_ID)}.

limit? is {IF_LIMIT}.
adjust? is {IF_ADJUST}.
move? is {IF_MOVE}.
create_voice? is {IF_CREATE_VOICE}.
create_text? is {IF_CREATE_TEXT}.

twitter account is {AUTH}.""",
                                        embed=embed)

    @app_commands.command()
    @app_commands.describe(user=_T('@User'))
    @help_command()
    async def profile(self,
                      interaction: discord.Interaction,
                      user: discord.User,
                      help: bool = False):
        """Show profile of spesific member.

        Parameters
        ----------
        interaction : discord.Interaction
            _description_
        user : str
            User to show.
        """
        GUILD_ID = interaction.guild_id

        # If PROFILE_ID is None, stop
        PROFILE_ID = get_profile_id(DATABASE_URL, GUILD_ID)
        if PROFILE_ID is None:
            await interaction.response.send_message("@Profile is not set.")
            return

        # Show profile
        channel = self.bot.get_channel(PROFILE_ID)

        messages = [message async for message in channel.history(limit=200, oldest_first=True)]
        message = get(messages, author=user)

        if message is not None:
            embed = discord.Embed(description=message.content)
            embed.set_author(name=user.nick or user.name,
                             icon_url=user.avatar)

            await interaction.response.send_message(embed=embed)
            return
        else:
            await interaction.response.send_message("No profile is found.")
            return

    async def sub_random(self,
                         interaction: discord.Interaction,
                         user: discord.User = None,
                         channel: discord.TextChannel = None,
                         filter_: str = None,
                         num: int = 1,
                         url_only: bool = True,
                         help: bool = False):
        await interaction.response.defer()

        if num == 0:
            num = np.infty

        if channel is None:
            channel = interaction.channel

        messages = [message async for message in channel.history(limit=200)]

        if user is not None:
            def func(message: discord.Message) -> bool:
                return message.author == user
            messages = list(filter(func, messages))

        def func(message: discord.Message) -> bool:
            return len(message.content) > 0
        messages = list(filter(func, messages))

        if url_only:
            def func(message: discord.Message) -> bool:
                return bool(re.search("https?://[0-9a-zA-Z/:%#\\$&\\?\\(\\)~\\.=\\+\\-]+",
                                      message.content))
            messages = list(filter(func, messages))

        if filter_:
            filter_ = filter_.strip()
            if filter_.startswith("-"):
                filter_ = filter_[1:].strip()

                def func(message: discord.Message) -> bool:
                    return filter_ not in message.content
            else:
                def func(message: discord.Message) -> bool:
                    return filter_ in message.content
            messages = list(filter(func, messages))

        NUM = len(messages)
        if NUM == 0:
            await interaction.followup.send(
                "No message is found.", ephemeral=True)
            return
        elif NUM > num:
            messages = random.sample(messages, num)

        def extract_url(message: discord.Message) -> str:
            return "\n".join(re.findall(
                "https?://[0-9a-zA-Z/:%#\\$&\\?\\(\\)~\\.=\\+\\-]+", message.content))

        message: discord.Message
        authors = list(set([message.author for message in messages]))
        embed = discord.Embed()
        if len(authors) == 1:
            author: discord.Member = authors[0]
            embed.set_author(name=author.display_name,
                             icon_url=author.avatar)
            for message in messages:
                embed.add_field(name=f"{message.author.display_name}",
                                value=message.content[:1024],
                                inline=False)
        else:
            embed.set_author(name="Multiple Users",
                             icon_url=interaction.guild.icon.url)
            for message in messages:
                embed.add_field(name=f"{message.author.display_name}",
                                value=message.content[:1024],
                                inline=False)

        if len(embed) > 2000:
            await interaction.followup.send("Too many entry.")
            return

        # urls = [extract_url(message) for message in messages]
        # links = "\n\n".join([url for url in urls if len(url) > 0])
        await interaction.followup.send(embed=embed,
                                        ephemeral=False)

    @app_commands.command()
    @app_commands.describe(user=_T('@User'), channel=_T('#TextChannel'))
    @help_command()
    async def random(self,
                     interaction: discord.Interaction,
                     user: discord.User = None,
                     channel: discord.TextChannel = None,
                     filter: str = None,
                     num: int = 1,
                     url_only: bool = True,
                     help: bool = False):
        """Show message randomly.

        Parameters
        ----------
        interaction : discord.Interaction
            _description_
        user : discord.User, optional
            User to show., by default None
            IF `None`, matching to all user.
        channel : discord.TextChannel, optional
            Channel where message is taken from, by default None
            If `None`, the channel where command used.
        filter : str, optional
            _description_, by default None
        num : int, optional
            Number of message to show, by default 1
        url_only: bool, optional
            Show only message contains URL.
        help : bool, optional
            _description_, by default False
        """
        await self.sub_random(interaction,
                              user=user,
                              channel=channel,
                              filter_=filter,
                              num=num,
                              url_only=url_only,
                              help=help)

    @app_commands.command()
    @app_commands.describe(channel=_T('#TextChannel'))
    @help_command()
    async def random_me(self,
                        interaction: discord.Interaction,
                        channel: discord.TextChannel = None,
                        filter: str = None,
                        num: int = 1,
                        url_only: bool = True,
                        help: bool = False):
        """Run `/radom user:@Me`.

        Parameters
        ----------
        interaction : discord.Interaction
            _description_
        channel : discord.TextChannel, optional
            Channel where message is taken from, by default None
            If `None`, the channel where command used.
        filter : str, optional
            _description_, by default None
        num : int, optional
            Number of message to show, by default 1
        url_only: bool, optional
            Show only message contains URL.
        help : bool, optional
            _description_, by default False
        """
        await self.sub_random(interaction,
                              user=interaction.user,
                              channel=channel,
                              filter_=filter,
                              num=num,
                              url_only=url_only,
                              help=help)

    @app_commands.command()
    @help_command()
    @has_permission(manage_messages=True)
    async def clean(self, interaction: discord.Interaction, help: bool = False):
        """Delete profile of leaved member.

        Previlage to manage messages is required.

        Parameters
        ----------
        interaction : discord.Interaction
            _description_
        """
        await interaction.response.defer()
        GUILD_ID = interaction.guild_id

        member_cand = ["Message from user following will be deleted."]
        message_cand = []
        PROFILE_ID = get_profile_id(DATABASE_URL, GUILD_ID)

        if PROFILE_ID is not None:
            channel = self.bot.get_channel(PROFILE_ID)
            m: discord.Message
            async for m in channel.history(limit=200, oldest_first=True):
                # skip if author is bot
                if m.author.bot:
                    continue

                # check if author is member
                res = await m.guild.query_members(user_ids=[m.author.id])
                if len(res) == 0:
                    member_cand.append(m.author.mention)
                    message_cand.append(m)

            if len(member_cand) > 1:
                confirm_content = f"YES, delete in {interaction.guild}."
                member_cand.append(
                    f"If you want to excute delete, plese type `{confirm_content}`.")
                await interaction.followup.send("\n".join(member_cand))

                def check(m):
                    """Check if it's the same user and channel."""
                    return m.author == interaction.user and m.channel == interaction.channel

                try:
                    response = await self.bot.wait_for('message', check=check, timeout=30.0)
                except asyncio.TimeoutError:
                    await interaction.followup.send("delete is canceled with timeout.")
                    return

                if response.content == confirm_content:
                    for m in message_cand:
                        await m.delete()
                    await interaction.followup.send("delete is excuted.")
                    return
                else:
                    await interaction.followup.send("delete is canceled.")
                    return

            else:
                await interaction.followup.send("No message to delete is found.")
                return
        else:
            await interaction.followup.send("@Profile is not set.")
            return

    @app_commands.command()
    @help_command()
    @has_permission(manage_messages=True)
    async def duplicate(self, interaction: discord.Interaction, help: bool = False):
        """Delete second or subsequent profile of same user.

        Previlage to manage messages is required.

        Parameters
        ----------
        interaction : discord.Interaction
            _description_
        """
        GUILD_ID = interaction.guild_id

        memberlist = []
        message_cand = []
        PROFILE_ID = get_profile_id(DATABASE_URL, GUILD_ID)
        if PROFILE_ID is not None:
            channel = self.bot.get_channel(PROFILE_ID)
            async for m in channel.history(limit=200, oldest_first=True):
                # skip if author is bot
                if m.author.bot:
                    continue

                # check if author is member
                if m.author.id in memberlist:
                    message_cand.append(m)
                else:
                    memberlist.append(m.author.id)

            if len(message_cand) > 0:
                confirm_content = f"YES, delete in {interaction.guild}."
                await interaction.response.send_message("If you want to excute delete, "
                                                        f"plese type `{confirm_content}`.")

                def check(m):
                    """Check if it's the same user and channel."""
                    return m.author == interaction.user and m.channel == interaction.channel

                try:
                    response = await self.bot.wait_for('message', check=check, timeout=30.0)
                except asyncio.TimeoutError:
                    await interaction.followup.send("delete is canceled with timeout.")
                    return

                if response.content == confirm_content:
                    for m in message_cand:
                        await m.delete()
                    await interaction.followup.send("delete is excuted.")
                    return
                else:
                    await interaction.followup.send("delete is canceled.")
                    return

            else:
                await interaction.response.send_message("No message to delete is found.")
                return
        else:
            await interaction.response.send_message("@Profile is not set.")
            return

    @ commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """Run on reaction is made.

        When a member with `@Senior` reacts on `#Profiles`,
        `@Freshman` is given to the person who sent the message.
        """
        GUILD_ID = payload.guild_id
        PROFILE_ID, LOG_ID, FRESHMAN_ID, SENIOR_ID, EMOJI_ID = get_pro_log_fre_sen_emo(DATABASE_URL,
                                                                                       GUILD_ID)
        if None in (PROFILE_ID,
                    FRESHMAN_ID,
                    SENIOR_ID) or payload.channel_id != PROFILE_ID:
            return

        emoji_id = payload.emoji.id or demojize(payload.emoji.name)
        if (EMOJI_ID is not None) and (emoji_id != EMOJI_ID):
            return

        FRESHMAN = get(payload.member.guild.roles, id=FRESHMAN_ID)
        if FRESHMAN is None:
            return

        channel = self.bot.get_channel(PROFILE_ID)
        message_id = payload.message_id
        message = await channel.fetch_message(message_id)
        member: discord.Member
        member, = await message.guild.query_members(user_ids=[message.author.id])

        if FRESHMAN in member.roles:
            return

        SENIOR = get(payload.member.roles, id=SENIOR_ID)
        if SENIOR is None:
            await message.remove_reaction(payload.emoji, payload.member)
            return

        await member.add_roles(FRESHMAN)

        if LOG_ID is None:
            return

        channel = self.bot.get_channel(LOG_ID)
        await channel.send(f"{payload.member.mention} "
                           f"add {FRESHMAN.mention} "
                           f"to {member.mention} via Aoi.")


async def setup(bot):
    await bot.add_cog(Profiles(bot))
