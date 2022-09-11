from discord import app_commands
from discord.app_commands import locale_str as _T
from discord.ext import commands
import discord
import re
import logging
import requests

from . import (
    get_database_url,
    help_command,
)
from .database import (
    get_github,
)


DATABASE_URL = get_database_url()
_log = logging.getLogger(__name__)


class Wiki(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @help_command()
    async def wiki(self,
                   interaction: discord.Interaction,
                   keyword: str = "Home",
                   help: bool = False):
        """Open github wiki page for `keyword`.

        Parameters
        ----------
        interaction : discord.Interaction
            _description_
        keyword : str
            _description_
        help : bool, optional
            _description_, by default False
        """
        GUILD_ID = interaction.guild_id
        await interaction.response.defer()

        keyword = keyword.strip()
        keyword_dash = keyword.replace(' ', '-')
        github = get_github(DATABASE_URL, GUILD_ID)
        if github is None:
            await interaction.followup.send("github need to set.")
            return

        url = f"https://github.com/{github}/wiki/{keyword_dash}"
        url_md = f"https://raw.githubusercontent.com/wiki/{github}/{keyword_dash}.md"

        response = requests.get(url_md)
        if response.ok:
            content = response.content.decode()

            def resolve_redirect(content):
                m = re.match("#REDIRECT \\[\\[(.+?)\\]\\]\n?$", content)
                if m:
                    redirect = m.group(1)
                    redirect_dash = redirect.replace(' ', '-')
                    url_md = f"https://raw.githubusercontent.com/wiki/{github}/{redirect_dash}.md"

                    response = requests.get(url_md)
                    if response.ok:
                        content = response.content.decode()

                        return resolve_redirect(content)
                    else:
                        return content
                else:
                    return content

            content = resolve_redirect(content)

            content = re.sub(
                "\\[\\[(.+?)\\]\\]",
                f"[\\1](https://github.com/{github}/wiki/\\1)",
                content)

            embed = discord.Embed(description=content)
            await interaction.followup.send(url,
                                            embed=embed)
        else:
            embed = discord.Embed(description="Not found.")
            await interaction.followup.send(url,
                                            embed=embed,
                                            ephemeral=True)


async def setup(bot):
    await bot.add_cog(Wiki(bot))
