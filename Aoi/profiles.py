from discord import app_commands
from discord.app_commands import locale_str as _T
from discord.ext import commands
from discord.utils import get
from emoji import demojize
import asyncio
import discord

from . import (
    convert_channel_to_mention,
    convert_role_to_mention,
    convert_user_to_mention,
    get_database_url,
)
from .database import (
    get_pre_pro_log_fre_sen_emo_ten_lim_adj,
    get_pro_log_fre_sen_emo,
    get_profile_id,
    update_emoji_id,
    update_freshman_id,
    update_log_id,
    update_prefix,
    update_profile_id,
    update_senior_id,
)

DATABASE_URL = get_database_url()


class Profiles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    async def detail(self, interaction: discord.Interaction):
        """Show detail of parameters."""
        await interaction.response.send_message("""Prefix is Prefix of command.
#Profile is Profile channel.
#Log is Log channel.
@Freshman is Role to assign to new member.
@Senior is Role who can assign to new member.
:emoji: is Emoji to assign role.

#Tenki is weather forecast channel.

limit? is Whether activate `/limit`.
adjust? is Wheter activate `on_voice_state_update`.""")

    @app_commands.command()
    async def status(self, interaction: discord.Interaction):
        """Show current config."""
        GUILD_ID = interaction.guild_id

        PREFIX, PROFILE_ID, LOG_ID, FRESHMAN_ID, SENIOR_ID, EMOJI_ID, TENKI_ID, IF_LIMIT, IF_ADJUST = \
            get_pre_pro_log_fre_sen_emo_ten_lim_adj(DATABASE_URL,
                                                    GUILD_ID)
        await interaction.response.send_message(f"""Prefix is `{PREFIX}`.
#Profile is {convert_channel_to_mention(PROFILE_ID)}.
#Log is {convert_channel_to_mention(LOG_ID)}.
@Freshman is {convert_role_to_mention(FRESHMAN_ID)}.
@Senior is {convert_role_to_mention(SENIOR_ID)}.
:emoji: is {EMOJI_ID}.

#Tenki is {convert_channel_to_mention(TENKI_ID)}.

limit? is {IF_LIMIT}.
adjust? is {IF_ADJUST}.""")
        return

    @app_commands.command()
    @app_commands.describe(prefix=_T('Prefix of command: Default prefix is `;`.'))
    async def setprefix(self, interaction: discord.Integration, prefix: str):
        """Change prefix.

        Previlage of administrator is required.
        """
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Previlage of administrator is required.")
            return

        GUILD_ID = interaction.guild_id

        prefix = str(prefix)
        update_prefix(DATABASE_URL, GUILD_ID, prefix)
        await interaction.response.send_message(f"Prefix is changed to `{prefix}`.")
        return

    @app_commands.command()
    @app_commands.describe(profile=_T('Profile channel: empty for disable.'))
    async def setprofile(self, interaction: discord.Integration, profile: discord.TextChannel = None):
        """Change #Profile.

        Previlage of administrator is required.
        """
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Previlage of administrator is required.")
            return

        GUILD_ID = interaction.guild_id

        if profile is None:
            update_profile_id(DATABASE_URL, GUILD_ID, profile)
            await interaction.response.send_message("#Profile is changed "
                                                    f"to {profile}.")
        else:
            update_profile_id(DATABASE_URL, GUILD_ID, profile.id)
            await interaction.response.send_message("#Profile is changed "
                                                    f"to {convert_channel_to_mention(profile.id)}.")
        return

    @app_commands.command()
    @app_commands.describe(log=_T('Log channel: empty for disable.'))
    async def setlog(self, interaction: discord.Integration, log: discord.TextChannel = None):
        """Change #Log.

        Previlage of administrator is required.
        """
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Previlage of administrator is required.")
            return

        GUILD_ID = interaction.guild_id

        if log is None:
            update_log_id(DATABASE_URL, GUILD_ID, log)
            await interaction.response.send_message("#Log is changed "
                                                    f"to {log}.")
        else:
            update_log_id(DATABASE_URL, GUILD_ID, log.id)
            await interaction.response.send_message("#Log is changed "
                                                    f"to {convert_channel_to_mention(log.id)}.")
        return

    @app_commands.command()
    @app_commands.describe(freshman=_T('Role to assign to new member: empty for disable.'))
    async def setfreshman(self, interaction: discord.Integration, freshman: discord.Role = None):
        """Change @Freshman.

        Previlage to manage roles is required.
        """
        if not interaction.user.guild_permissions.manage_roles:
            await interaction.response.send_message("Previlage to manage roles is required.")
            return

        GUILD_ID = interaction.guild_id

        if freshman is None:
            update_freshman_id(DATABASE_URL, GUILD_ID, freshman)
            await interaction.response.send_message("@Freshman is changed "
                                                    f"to {freshman}.")
        else:
            update_freshman_id(DATABASE_URL, GUILD_ID, freshman.id)
            await interaction.response.send_message("@Freshman is changed "
                                                    f"to {convert_role_to_mention(freshman.id)}.")
        return

    @app_commands.command()
    @app_commands.describe(
        senior=_T('Role who can assign to new member: empty for disable.'))
    async def setsenior(self, interaction: discord.Integration, senior: discord.Role = None):
        """Change @Senior.

        Previlage to manage roles is required.
        """
        if not interaction.user.guild_permissions.manage_roles:
            await interaction.response.send_message("Previlage to manage roles is required.")
            return

        GUILD_ID = interaction.guild_id

        if senior is None:
            update_senior_id(DATABASE_URL, GUILD_ID, senior)
            await interaction.response.send_message("@Senior is changed "
                                                    f"to {senior}.")
        else:
            update_senior_id(DATABASE_URL, GUILD_ID, senior.id)
            await interaction.response.send_message("@Senior is changed "
                                                    f"to {convert_role_to_mention(senior.id)}.")
        return

    @app_commands.command()
    @app_commands.describe(emoji=_T('Emoji to assign role: empty for matching all.'))
    async def setemoji(self, interaction: discord.Integration, emoji: str = None):
        """Change :emoji:.

        Previlage of manage roles is required.
        """
        if not interaction.user.guild_permissions.manage_roles:
            await interaction.response.send_message("Previlage to manage roles is required.")
            return

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
    @app_commands.describe(user=_T('@User'))
    async def profile(self, interaction: discord.Interaction, user: discord.User):
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

    @app_commands.command()
    async def clean(self, interaction: discord.Interaction):
        """Delete profile of leaved member.

        Previlage to manage messages is required.

        Parameters
        ----------
        interaction : discord.Interaction
            _description_
        """
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("Previlage to manage messages is required")
            return

        await interaction.response.defer()
        GUILD_ID = interaction.guild_id

        member_cand = ["Message from user following will be deleted."]
        message_cand = []
        PROFILE_ID = get_profile_id(DATABASE_URL, GUILD_ID)
        if PROFILE_ID is not None:
            channel = self.bot.get_channel(PROFILE_ID)
            async for m in channel.history(limit=200, oldest_first=True):
                # skip if author is bot
                if m.author.bot:
                    continue

                # check if author is member
                res = await m.guild.query_members(user_ids=[m.author.id])
                if len(res) == 0:
                    member_cand.append(convert_user_to_mention(m.author.id))
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
    async def duplicate(self, interaction: discord.Interaction):
        """Delete second or subsequent profile of same user.

        Previlage to manage messages is required.

        Parameters
        ----------
        interaction : discord.Interaction
            _description_
        """
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("Previlage to manage messages is required")
            return

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
        await channel.send(f"{convert_user_to_mention(payload.member.id)} "
                           f"add {convert_role_to_mention(FRESHMAN_ID)} "
                           f"to {convert_user_to_mention(member.id)} via Aoi.")


async def setup(bot):
    await bot.add_cog(Profiles(bot))
