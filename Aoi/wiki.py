from __future__ import annotations
from discord import app_commands
import Levenshtein
from functools import wraps
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


def stripper_keyword(func):
    @wraps(func)
    def wrapper(*args, keyword, **kwargs):
        return func(*args, keyword=keyword.strip(), **kwargs)
    return wrapper


class GitHub_Wiki():
    def __init__(self, repo):
        self.repo = repo
        self._index = None
        self.status = False

    @classmethod
    @stripper_keyword
    def normalized(cls, *, keyword: str):
        keyword = keyword.lower()
        return keyword.replace(" ", "")

    @property
    def index(self) -> list:
        if self._index is None:
            response = requests.get(self.url_md_footer)
            if response.ok:
                content = response.content.decode()
                self._index = list(re.findall("\\[\\[(.+?)\\]\\]", content))
            else:
                self._index = []
        return self._index

    @stripper_keyword
    def url(self, *, keyword: str) -> str:
        keyword = keyword.replace(' ', '-')
        return f"https://github.com/{self.repo}/wiki/{keyword}"

    @stripper_keyword
    def url_search(self, *, keyword: str) -> str:
        keyword = keyword.replace(' ', '%20')
        return f"https://github.com/{self.repo}/search?q={keyword}&type=wikis"

    @stripper_keyword
    def url_md(self, *, keyword: str) -> str:
        keyword = keyword.replace(' ', '-')
        return f"https://raw.githubusercontent.com/wiki/{self.repo}/{keyword}.md"

    @property
    def url_md_footer(self) -> str:
        return self.url_md(keyword="_Footer")

    @stripper_keyword
    def search_index(self, *, keyword: str, num=3) -> list:
        def func(x):
            return Levenshtein.distance(keyword, x)
        return sorted(self.index, key=func)[:num]

    @stripper_keyword
    def content(self, *, keyword: str, default: str = None) -> str:
        if default is None:
            self.status = False

        response = requests.get(self.url_md(keyword=keyword))
        if response.ok:
            self.status = True
            content = response.content.decode()

            m = re.match("#REDIRECT \\[\\[(.+?)\\]\\]\n?$", content)
            if m:
                redirect = m.group(1)
                content = self.content(keyword=redirect, default=content)
        else:
            if default:
                content = default
            else:
                cand = self.search_index(keyword=keyword)
                if len(cand) > 0:
                    wordlist = '\n'.join([f"* [[{c}]]" for c in cand])
                    content = f"""Not Found.

May be following.
{wordlist}

Or [Search {keyword} in GitHub?]({self.url_search(keyword=keyword)})"""

                    redirect = cand[0]
                    if redirect != keyword and \
                            self.normalized(keyword=redirect) == self.normalized(keyword=keyword):
                        content = self.content(
                            keyword=redirect, default=content)
                else:
                    content = f"""[Not Found.

Search {keyword} in GitHub?]({self.url_search(keyword=keyword)})"""

        return re.sub("\\[\\[(.+?)\\]\\]",
                      f"[\\1](https://github.com/{self.repo}/wiki/\\1)",
                      content)


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

        github = get_github(DATABASE_URL, GUILD_ID)
        if github is None:
            await interaction.followup.send("github need to set.")
            return

        wiki = GitHub_Wiki(github)
        url = wiki.url(keyword=keyword)
        content = wiki.content(keyword=keyword)
        embed = discord.Embed(description=content)
        await interaction.followup.send(url,
                                        embed=embed,
                                        ephemeral=not wiki.status)


async def setup(bot):
    await bot.add_cog(Wiki(bot))
