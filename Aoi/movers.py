from multiprocessing.connection import wait
from unicodedata import name
from discord import app_commands
from discord.app_commands import locale_str as _T
from discord.ext import commands
import discord
import random
from discord.utils import get

from . import (
    convert_channel_to_mention,
    convert_user_to_mention,
    get_database_url,
    help_command,
)
from .database import (
    get_if_adjust,
    get_if_limit,
    update_if_adjust,
    update_if_limit,
)


def get_if_create_voice(DATABASE_URL, GUILD_ID):
    return False


def get_if_create_text(DATABASE_URL, GUILD_ID):
    return False


DATABASE_URL = get_database_url()


class Movers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.describe(voice_channel=_T('#Voice_Channel, empty for here.'))
    @help_command()
    async def move(self, interaction: discord.Interaction, voice_channel: discord.VoiceChannel = None, help: bool = False):
        """Move all members to another voice channel.

        Parameters
        ----------
        interaction : discord.Interaction
            _description_
        channel : discord.VoiceChannel, optional
            Voice channel to move.
            `None` to move to the channel where message create.
        help : bool, optional
            Wether to show help instead, by default False
        """
        origin = interaction.user.voice.channel

        if voice_channel is None:
            voice_channel = interaction.channel

        for member in origin.members:
            await member.move_to(voice_channel)

        await interaction.response.send_message(f"All members are move to {convert_channel_to_mention(voice_channel.id)}.")

    @app_commands.command()
    @app_commands.describe(voice_channel=_T('#Voice_Channel, empty for here.'))
    @help_command()
    async def split(self, interaction: discord.Interaction, voice_channel: discord.VoiceChannel = None, help: bool = False):
        """Move random half of members to another voice channel.

        Parameters
        ----------
        interaction : discord.Interaction
            _description_
        voice_channel : discord.VoiceChannel, optional
            Voice channel to move.
            `None` to move to the channel where message create.
        help : bool, optional
            Wether to show help instead, by default False
        """
        origin = interaction.user.voice.channel

        if voice_channel is None:
            voice_channel = interaction.channel

        members = [
            member for member in origin.members if not member.bot]
        members = random.sample(members, len(members))
        members1 = members[:len(members) // 2]
        members2 = members[len(members) // 2:]

        text = []
        text.append(
            f"> Members for {convert_channel_to_mention(origin.id)}")
        for member in members1:
            text.append(f"{convert_user_to_mention(member.id)}")
        text.append(
            f"> Members for {convert_channel_to_mention(voice_channel.id)}")
        for member in members2:
            text.append(f"{convert_user_to_mention(member.id)}")
            await member.move_to(voice_channel)

        await interaction.response.send_message("\n".join(text))

    @app_commands.command()
    @app_commands.describe(voice_channel=_T('#Voice_Channel, empty for here.'))
    @help_command()
    async def shuffle(self, interaction: discord.Interaction, voice_channel: discord.VoiceChannel = None, help: bool = False):
        """Shuffle members with another voice channel.

        Parameters
        ----------
        interaction : discord.Interaction
            _description_
        voice_channel : discord.VoiceChannel, optional
            Voice channel to move.
            `None` to move to the channel where message create.
        help : bool, optional
            Wether to show help instead, by default False
        """
        origin = interaction.user.voice.channel

        if voice_channel is None:
            voice_channel = interaction.channel

        members = [
            member for member in origin.members if not member.bot] + [
            member for member in voice_channel.members if not member.bot]
        members = random.sample(members, len(members))
        members1 = members[:len(members) // 2]
        members2 = members[len(members) // 2:]

        text = []
        text.append(
            f"> Members for {convert_channel_to_mention(origin.id)}")
        for member in members1:
            text.append(f"{convert_user_to_mention(member.id)}")
            await member.move_to(origin)
        text.append(
            f"> Members for {convert_channel_to_mention(voice_channel.id)}")
        for member in members2:
            text.append(f"{convert_user_to_mention(member.id)}")
            await member.move_to(voice_channel)

        await interaction.response.send_message("\n".join(text))

    @app_commands.command()
    @app_commands.describe(limit=_T("Value of `0` to remove limit, empty for 0."))
    @help_command()
    async def limit(self, interaction: discord.Interaction, limit: int = 0, help: bool = False):
        """Change upper limit of voice channel which you join.

        Parameters
        ----------
        interaction : discord.Interaction
            _description_
        limit : int, optional
            _description_, by default 0
        help : bool, optional
            Wether to show help instead, by default False
        """
        channel = interaction.user.voice.channel
        GUILD_ID = interaction.guild_id

        if channel is None:
            await interaction.response.send_message("You do not join voice channel.")
            return
        elif get_if_limit(DATABASE_URL, GUILD_ID):
            await channel.edit(user_limit=limit)
            await interaction.response.send_message(f"Upper limit is changed to {limit}.")
        else:
            await interaction.response.send_message("Need limit? changed to `True`.")
            return

    @app_commands.command()
    @app_commands.describe(enable=_T('Whether activate `/limit`.'))
    @help_command()
    async def setlimit(self, interaction: discord.Integration, enable: bool, help: bool = False):
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
        if not interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message("Previlage to manage channels is required.")
            return

        GUILD_ID = interaction.guild_id

        update_if_limit(DATABASE_URL, GUILD_ID, enable)
        await interaction.response.send_message(f"limit? is changed to `{enable}`.")
        return

    @app_commands.command()
    @app_commands.describe(enable=_T('Wheter activate `on_voice_state_update`.'))
    @help_command()
    async def setadjust(self, interaction: discord.Integration, enable: bool, help: bool = False):
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
        if not interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message("Previlage to manage channels is required.")
            return

        GUILD_ID = interaction.guild_id

        update_if_adjust(DATABASE_URL, GUILD_ID, enable)
        await interaction.response.send_message(f"adjust? is changed to `{enable}`.")
        return

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        """Run on member join or leave voice channel."""
        # On leave
        if before.channel is not None:
            GUILD_ID = before.channel.guild.id
            # Adjust on Bot
            if member.bot and before.channel.user_limit != 0 and get_if_adjust(DATABASE_URL,
                                                                               GUILD_ID):
                await before.channel.edit(user_limit=before.channel.user_limit - 1)
            # Destroy or message
            if get_if_create_voice(DATABASE_URL, GUILD_ID) and \
                not before.channel.name.endswith("_") and \
                    before.channel.name.count("/"):
                if_create_text = get_if_create_text(DATABASE_URL, GUILD_ID)
                if if_create_text:
                    text_chann = get(before.channel.guild.text_channels,
                                     topic=f"Aoi - {before.channel.id}")
                    await text_chann.set_permissions(member,
                                                     overwrite=None)
                    await before.channel.set_permissions(member,
                                                         overwrite=None)
                else:
                    text_chann = before.channel
                    await text_chann.set_permissions(member,
                                                     overwrite=None)

                embed = discord.Embed()
                embed.set_author(name=f"{member.display_name} - left",
                                 icon_url=member.display_avatar)
                await text_chann.send(embed=embed)

                if len(before.channel.members) == 0:
                    await before.channel.delete()
                    if if_create_text:
                        await text_chann.delete()

        # On join
        if after.channel is not None:
            GUILD_ID = after.channel.guild.id
            # Adjust on Bot
            if member.bot and after.channel.user_limit != 0 and get_if_adjust(DATABASE_URL,
                                                                              GUILD_ID):
                await after.channel.edit(user_limit=after.channel.user_limit + 1)
            # Create or message
            if get_if_create_voice(DATABASE_URL, GUILD_ID) and \
                    not after.channel.name.endswith("_"):
                if_create_text = get_if_create_text(DATABASE_URL, GUILD_ID)
                if after.channel.name.count("/"):
                    if if_create_text:
                        text_chann = get(after.channel.guild.text_channels,
                                         topic=f"Aoi - {after.channel.id}")
                        await text_chann.set_permissions(member,
                                                         overwrite=discord.PermissionOverwrite(read_messages=True))
                    else:
                        text_chann = after.channel

                    if len(after.channel.members) == 1:
                        await after.channel.set_permissions(member,
                                                            manage_channels=True,
                                                            move_members=True)
                        embed = discord.Embed(
                            description=after.channel.mention)
                        embed.set_author(name=f"{member.display_name} - create",
                                         icon_url=member.display_avatar)
                        await text_chann.send(embed=embed)
                    else:
                        embed = discord.Embed()
                        embed.set_author(name=f"{member.display_name} - joined",
                                         icon_url=member.display_avatar)
                        await text_chann.send(embed=embed)

                else:
                    if len(after.channel.members) == 1:
                        i = 1
                        while get(after.channel.guild.voice_channels,
                                  name=f"{after.channel.name} / {i}"):
                            i += 1
                        new_name = f"{after.channel.name} / {i}"
                        new_chan = await after.channel.clone(name=new_name)

                        if if_create_text:
                            overwrites = {
                                after.channel.guild.default_role: discord.PermissionOverwrite(
                                    read_messages=False),
                                member: discord.PermissionOverwrite(
                                    read_messages=True),
                            }
                            await after.channel.guild.create_text_channel(name=new_name.replace(" / ", "-"),
                                                                          topic=f"Aoi - {new_chan.id}",
                                                                          overwrites=overwrites)

                        for member in after.channel.members:
                            await member.move_to(new_chan)


async def setup(bot):
    await bot.add_cog(Movers(bot))
