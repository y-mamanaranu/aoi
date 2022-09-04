from discord.ext import commands
from discord import app_commands
import discord
from discord.app_commands import locale_str as _T
from . import (convert_user_to_mention,
               get_database_url,
               update_if_limit,
               get_if_adjust,
               get_if_limit,
               update_if_adjust,
               convert_channel_to_mention)
import random


DATABASE_URL = get_database_url()


class Movers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.describe(voice_channel=_T('#Voice_Channel: empty for here.'))
    async def move(self, interaction: discord.Interaction, voice_channel: discord.VoiceChannel = None):
        """Move all members to another voice channel.

        Parameters
        ----------
        interaction : discord.Interaction
            _description_
        channel : discord.VoiceChannel, optional
            Voice channel to move.
            `None` to move to the channel where message create.
        """
        origin = interaction.user.voice.channel

        if voice_channel is None:
            voice_channel = interaction.channel

        for member in origin.members:
            await member.move_to(voice_channel)

        await interaction.response.send_message(f"All members are move to {convert_channel_to_mention(voice_channel.id)}.")

    @app_commands.command()
    @app_commands.describe(voice_channel=_T('#Voice_Channel: empty for here.'))
    async def split(self, interaction: discord.Interaction, voice_channel: discord.VoiceChannel = None):
        """Move random half of members to another voice channel.

        Parameters
        ----------
        interaction : discord.Interaction
            _description_
        voice_channel : discord.VoiceChannel, optional
            Voice channel to move.
            `None` to move to the channel where message create.
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
    @app_commands.describe(voice_channel=_T('#Voice_Channel: empty for here.'))
    async def shuffle(self, interaction: discord.Interaction, voice_channel: discord.VoiceChannel = None):
        """Shuffle members with another voice channel.

        Parameters
        ----------
        interaction : discord.Interaction
            _description_
        voice_channel : discord.VoiceChannel, optional
            Voice channel to move.
            `None` to move to the channel where message create.
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
    @app_commands.describe(limit=_T("Value of `0` to remove limit: empty for 0."))
    async def limit(self, interaction: discord.Interaction, limit: int = 0):
        """Change upper limit of voice channel which you join."""
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
    async def setlimit(self, interaction: discord.Integration, enable: bool):
        """Change limit?.

        Previlage to manage channels is required.
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
    async def setadjust(self, interaction: discord.Integration, enable: bool):
        """Change adjust?.

        Previlage to manage channels is required.
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
        if member.bot:
            if before.channel is not None and before.channel.user_limit != 0:
                GUILD_ID = before.channel.guild.id
                if get_if_adjust(DATABASE_URL, GUILD_ID):
                    await before.channel.edit(user_limit=before.channel.user_limit - 1)
            if after.channel is not None and after.channel.user_limit != 0:
                GUILD_ID = after.channel.guild.id
                if get_if_adjust(DATABASE_URL, GUILD_ID):
                    await after.channel.edit(user_limit=after.channel.user_limit + 1)


async def setup(bot):
    await bot.add_cog(Movers(bot))
