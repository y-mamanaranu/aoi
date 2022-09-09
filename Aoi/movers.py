from distutils.dir_util import create_tree
from discord import app_commands
from discord.app_commands import locale_str as _T
from discord.ext import commands
import discord
import random
from discord.utils import get
import re

from . import (
    get_database_url,
    help_command,
    SearchText
)
from .database import (
    get_if_adjust,
    get_if_limit,
    get_icv_ict,
    get_if_move,
)


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
        GUILD_ID = interaction.guild_id
        if not get_if_move(DATABASE_URL, GUILD_ID):
            await interaction.response.send_message("Change move? to `True` to use this command.")
            return

        await interaction.response.defer()
        origin = interaction.user.voice.channel

        if voice_channel is None:
            voice_channel = interaction.channel

        if_create_voice, if_create_text = get_icv_ict(DATABASE_URL, GUILD_ID)
        if if_create_voice:
            voice_channel = await self.sub_create_voice(interaction.user,
                                                        voice_channel,
                                                        if_create_text,
                                                        force=True)
        for member in sorted(origin.members, key=lambda x: x.bot):
            await member.move_to(voice_channel)
        await interaction.followup.send(f"All members are move to {voice_channel.mention}.")

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
        GUILD_ID = interaction.guild_id
        if not get_if_move(DATABASE_URL, GUILD_ID):
            await interaction.response.send_message("Change move? to `True` to use this command.")
            return

        await interaction.response.defer()
        origin = interaction.user.voice.channel

        if voice_channel is None:
            voice_channel = interaction.channel

        members = [
            member for member in origin.members if not member.bot]
        members = random.sample(members, len(members))
        members1 = members[:len(members) // 2]
        members2 = members[len(members) // 2:]

        if interaction.user in members1:
            members1, members2 = members2, members1

        if_create_voice, if_create_text = get_icv_ict(DATABASE_URL, GUILD_ID)
        if if_create_voice:
            voice_channel = await self.sub_create_voice(interaction.user,
                                                        voice_channel,
                                                        if_create_text,
                                                        force=True)

        for member in members2:
            await member.move_to(voice_channel)

        text = []
        text.append(f"> Half of members move to {voice_channel.mention}.")
        text.append(f"> Members for {origin.mention}")
        for member in members1:
            text.append(f"{member.mention}")
        text.append(f"> Members for {voice_channel.mention}")
        for member in members2:
            text.append(f"{member.mention}")

        await interaction.followup.send("\n".join(text))

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
        GUILD_ID = interaction.guild_id
        if not get_if_move(DATABASE_URL, GUILD_ID):
            await interaction.response.send_message("Change move? to `True` to use this command.")
            return

        await interaction.response.defer()
        origin = interaction.user.voice.channel

        if voice_channel is None:
            voice_channel = interaction.channel

        members = [
            member for member in origin.members if not member.bot] + [
            member for member in voice_channel.members if not member.bot]
        members = random.sample(members, len(members))
        members1 = members[:len(members) // 2]
        members2 = members[len(members) // 2:]

        if interaction.user in members2:
            members1, members2 = members2, members1

        if_create_voice, if_create_text = get_icv_ict(DATABASE_URL, GUILD_ID)
        if if_create_voice:
            voice_channel = await self.sub_create_voice(members2[0],
                                                        voice_channel,
                                                        if_create_text,
                                                        force=True)

        # Keep voice_channel not empty
        for member in members2:
            await member.move_to(voice_channel)
        for member in members1:
            await member.move_to(origin)

        text = []
        text.append(f"> Shuffle members with {voice_channel.mention}.")
        text.append(f"> Members for {origin.mention}")
        for member in members1:
            text.append(f"{member.mention}")
        text.append(f"> Members for {voice_channel.mention}")
        for member in members2:
            text.append(f"{member.mention}")

        await interaction.followup.send("\n".join(text))

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
    @app_commands.describe()
    @help_command()
    async def need_owner(self, interaction: discord.Interaction, help: bool = False):
        vocie_chann = interaction.user.voice.channel
        if vocie_chann is None or not vocie_chann.name.count("/"):
            await interaction.response.send_message(
                "You doesn't join auto created channel.")
            return

        GUILD_ID = interaction.guild_id
        _, if_create_text = get_icv_ict(DATABASE_URL,
                                        GUILD_ID)
        if if_create_text:
            text_chann = get(vocie_chann.guild.text_channels,
                             topic=SearchText(f"^Aoi - {vocie_chann.mention}&<@\\d+>$"))
            owner_id = int(re.match(f"^Aoi - {vocie_chann.mention}&<@(\\d+)>$",
                                    text_chann.topic).group(1))
            owner = get(vocie_chann.members, id=owner_id)
        else:
            text_chann = vocie_chann
            owner = None

        if owner is None:
            def func(member: discord.Member):
                return vocie_chann.permissions_for(member).manage_channels

            members = list(filter(func, vocie_chann.members))
            if len(members):
                owner: discord.Member = members[0]

        if owner is not None:
            await interaction.response.send_message(
                f"{owner.mention} is already owner.")
            return

        def func(member: discord.Member):
            return not member.bot
        members = list(filter(func, vocie_chann.members))
        new_owner: discord.Member = members[0]

        embed = discord.Embed()
        embed.set_author(name=f"{new_owner.display_name} - become owner",
                         icon_url=new_owner.display_avatar)
        message = await text_chann.send(embed=embed)
        if if_create_text:
            await message.pin()
        await vocie_chann.set_permissions(new_owner,
                                          move_members=True,
                                          manage_channels=True)
        if if_create_text and text_chann:
            await text_chann.set_permissions(new_owner,
                                             read_messages=True,
                                             manage_channels=True)
        await interaction.response.send_message(
            f"{new_owner.mention} become owner.")

    async def sub_create_voice(self,
                               member: discord.Member,
                               vocie_chann: discord.VoiceChannel,
                               if_create_text: bool,
                               force: bool = False):
        if vocie_chann.name.endswith("_"):
            return vocie_chann
        else:
            if vocie_chann.name.count("/"):
                if if_create_text:
                    text_chann = get(vocie_chann.guild.text_channels,
                                     topic=SearchText(f"^Aoi - {vocie_chann.mention}&<@\\d+>$"))
                    if len(vocie_chann.members) > 1:
                        await text_chann.set_permissions(member,
                                                         overwrite=discord.PermissionOverwrite(read_messages=True))
                else:
                    text_chann = vocie_chann

                embed = discord.Embed()
                embed.set_author(name=f"{member.display_name} - joined",
                                 icon_url=member.display_avatar)
                await text_chann.send(embed=embed)

                return vocie_chann
            else:
                if len(vocie_chann.members) == 1 or force:
                    name = vocie_chann.name.replace('/', '')
                    owner = member.display_name.replace('/', '')
                    new_name = f"{name} / {owner}"
                    new_chan = await vocie_chann.clone(name=new_name)

                    if if_create_text:
                        overwrites = {
                            vocie_chann.guild.default_role: discord.PermissionOverwrite(
                                read_messages=False),
                            member: discord.PermissionOverwrite(
                                read_messages=True),
                        }
                        text_chann = await vocie_chann.guild.create_text_channel(name=f"{name}-{owner}",
                                                                                 topic=f"Aoi - {new_chan.mention}&{member.mention}",
                                                                                 overwrites=overwrites,
                                                                                 category=new_chan.category)
                        await new_chan.send(f"Please use {text_chann.mention}")
                    else:
                        text_chann = new_chan

                    await new_chan.set_permissions(member,
                                                   move_members=True,
                                                   manage_channels=True)
                    if if_create_text and text_chann:
                        await text_chann.set_permissions(member,
                                                         read_messages=True,
                                                         manage_channels=True)

                    embed = discord.Embed(
                        description=f"{new_chan.mention} [[Click Here]]({new_chan.jump_url})")
                    embed.set_author(name=f"{member.display_name} - create",
                                     icon_url=member.display_avatar)
                    message = await text_chann.send(embed=embed)
                    if if_create_text:
                        await message.pin()

                    notify_chann = get(vocie_chann.guild.text_channels,
                                       topic=SearchText(f"^Aoi = {vocie_chann.mention}: .*$", flags=re.MULTILINE))
                    if notify_chann is not None:
                        match = re.search(f"^Aoi = {vocie_chann.mention}: (.*)$",
                                          notify_chann.topic,
                                          flags=re.MULTILINE)
                        if match:
                            text = match.group(1).strip()

                            embed = discord.Embed()
                            embed.set_author(name=f"{member.display_name}",
                                             icon_url=member.display_avatar)
                            if vocie_chann.category is not None:
                                embed.add_field(name="Category",
                                                value=vocie_chann.category,
                                                inline=True)
                            embed.add_field(name="Channel",
                                            value=f"{new_chan.mention} [[Click Here]]({new_chan.jump_url})",
                                            inline=True)
                            await notify_chann.send(text if len(text) else None,
                                                    embed=embed)

                    for member in vocie_chann.members:
                        await member.move_to(new_chan)

                    return new_chan
                else:
                    return vocie_chann

    async def sub_delete_vocie(self,
                               member: discord.Member,
                               vocie_chann: discord.VoiceChannel,
                               if_create_text: bool):
        if not vocie_chann.name.endswith("_") and \
                vocie_chann.name.count("/"):
            if if_create_text:
                text_chann = get(vocie_chann.guild.text_channels,
                                 topic=SearchText(f"^Aoi - {vocie_chann.mention}&<@\\d+>$"))
                if text_chann:
                    await text_chann.set_permissions(member,
                                                     overwrite=None)
                await vocie_chann.set_permissions(member,
                                                  overwrite=None)
            else:
                text_chann = vocie_chann
                await text_chann.set_permissions(member,
                                                 overwrite=None)

            if text_chann:
                embed = discord.Embed()
                embed.set_author(name=f"{member.display_name} - left",
                                 icon_url=member.display_avatar)
                await text_chann.send(embed=embed)

            if len(vocie_chann.members) == 0:
                await vocie_chann.delete()
                if if_create_text and text_chann:
                    await text_chann.delete()

    async def sub_adjust_voice(self,
                               member: discord.Member,
                               vocie_chann: discord.VoiceChannel,
                               leave: bool = False):
        if member.bot and vocie_chann.user_limit != 0:
            await vocie_chann.edit(user_limit=vocie_chann.user_limit + [1, -1][int(leave)])

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        """Run on member join or leave voice channel."""
        if before.channel == after.channel:
            return

        # On join
        if after.channel is not None:
            GUILD_ID = after.channel.guild.id
            if_create_voice, if_create_text = get_icv_ict(DATABASE_URL,
                                                          GUILD_ID)

            if get_if_adjust(DATABASE_URL, GUILD_ID):
                await self.sub_adjust_voice(member, after.channel)

            if if_create_voice:
                await self.sub_create_voice(member, after.channel, if_create_text)

        # On leave
        if before.channel is not None:
            GUILD_ID = before.channel.guild.id
            if_create_voice, if_create_text = get_icv_ict(DATABASE_URL,
                                                          GUILD_ID)

            if get_if_adjust(DATABASE_URL, GUILD_ID):
                await self.sub_adjust_voice(member, before.channel, leave=True)

            if if_create_voice:
                await self.sub_delete_vocie(member, before.channel, if_create_text)


async def setup(bot):
    await bot.add_cog(Movers(bot))
