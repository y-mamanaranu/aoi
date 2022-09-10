from __future__ import annotations
import os
import re
import pydoc
import inspect
from functools import wraps
import discord
import numpy as np
import datetime

JST = datetime.timezone(datetime.timedelta(hours=9), name='JST')


def help_command():
    def _help_command(func):
        params = inspect.signature(func).parameters
        i = list(params.keys()).index("interaction")

        @wraps(func)
        async def wrapper(*args, **kwargs):
            if kwargs.get("help"):
                interaction: discord.Interaction = args[i]
                embed = discord.Embed(description=pydoc.render_doc(func))
                await interaction.response.send_message(embed=embed)
            else:
                return await func(*args, **kwargs)
        return wrapper
    return _help_command


def has_permission(**kwargs):
    def _has_permission(func):
        params = inspect.signature(func).parameters
        i = list(params.keys()).index("interaction")
        required = kwargs

        @wraps(func)
        async def wrapper(*args, **kwargs):
            interaction: discord.Interaction = args[i]
            actual = dict(iter(interaction.user.guild_permissions))
            if not all([actual[key] for key in required.keys()]):
                return await interaction.response.send_message(f"Previlage is required: {', '.join(required.keys())}.",
                                                               ephemeral=True)
            else:
                return await func(*args, **kwargs)
        return wrapper
    return _has_permission


def convert_mention_to_user(mention: str):
    """Convert mention to user to user_id."""
    res = re.match(r"^<@\!?(\d+)>$", mention)
    if res is None:
        return mention
    else:
        return res.group(1)


def convert_mention_to_channel(mention: str):
    """Convert mention to channel to profile_id."""
    res = re.match(r"^<#(\d+)>$", mention)
    if res is None:
        return mention
    else:
        return res.group(1)


def convert_mention_to_role(mention: str):
    """Convert mention to role to freshman_id."""
    res = re.match(r"^<@&(\d+)>$", mention)
    if res is None:
        return mention
    else:
        return res.group(1)


def convert_user_to_mention(user_id: str):
    """Convert user_id mention to user."""
    if user_id is None:
        return None

    return f"<@{user_id}>"


def convert_channel_to_mention(profile_id: str):
    """Convert profile_id to mention to channel."""
    if profile_id is None:
        return None

    return f"<#{profile_id}>"


def convert_role_to_mention(freshman_id: str):
    """Convert freshman_id mention to role."""
    if freshman_id is None:
        return None

    return f"<@&{freshman_id}>"


def get_token():
    """Get token of Discord bot."""
    return os.environ["TOKEN"]


def get_database_url():
    """Get database URL of Heroku Postgres."""
    return os.environ["DATABASE_URL"]


def get_twitter_consumer_key():
    """Get consumer_key of Twitter."""
    return os.environ["TWITTER_CONSUMER_KEY"]


def get_twitter_consumer_secret():
    """Get twitter_consumer_secret of Twitter."""
    return os.environ["TWITTER_CONSUMER_SECRET"]


class SearchText(object):
    def __init__(self, value, flags=0):
        self.pattern = re.compile(value, flags=flags)

    def __eq__(self, value: str):
        if isinstance(value, str):
            return bool(self.pattern.search(value))
        if isinstance(value, self.__class__):
            return self.pattern == value.pattern
        else:
            return False


def calc_level(sec: int) -> int:
    """Level `n` requires `2**(n-1)` hours."""
    hour = np.clip(sec // 3600, 0.5, None)
    return int(1 + np.log2(hour) // 1)


def calc_hour(level: int) -> int:
    """Level `n` requires `2**(n-1)` hours."""
    if level <= 0:
        return 0
    else:
        return 2**(level - 1)


def get_delta(tzinfo: datetime.timezone = JST):
    """"""
    now = datetime.datetime.now(tzinfo)
    target = datetime.datetime(now.year,
                               now.month,
                               now.day + int(now.hour >= 5),
                               5,
                               0,
                               0,
                               tzinfo=tzinfo)
    print(f"Now: {now}.")
    print(f"Target: {target}.")
    return (target.timestamp() - now.timestamp())


class Custum_Parser(object):
    def __init__(self, prefix: str, suffix: str):
        self.prefix = prefix
        self.suffix = suffix

    @classmethod
    def from_string(cls, setting: str) -> Custum_Parser:
        setting = setting.strip()
        res = re.match("^(.*)__key__(.*)__value__$", setting)
        if res is None:
            return None
        else:
            return Custum_Parser(*res.groups())

    def load(self, text: str) -> dict:
        """Load `text` as `dict`.

        Parameters
        ----------
        text : str
            _description_

        Returns
        -------
        dict
            _description_

        Sample
        ------
        setting="<prefix>__key__<suffix>__value__"

        sample=```<prefix>key1<suffix>value1
        <prefix>key2<suffix>value2
        <prefix>key3<suffix>value3
        <prefix>key_multiline1<suffix>value_multiline1-1
        value_multiline1-2
        value_multiline1-3
        <prefix>key_multiline2<suffix>value_multiline2-1
        value_multiline2-2
        value_multiline2-3
        ```

        p = Custum_Parser.from_string(setting)
        p.load(sample)
        > {'key1': 'value1',
        >  'key2': 'value2',
        >  'key3': 'value3',
        >  'key_multiline1': 'value_multiline1-1\nvalue_multiline1-2\nvalue_multiline1-3',
        >  'key_multiline2': 'value_multiline2-1\nvalue_multiline2-2\nvalue_multiline2-3'}
        ```
        """
        text.strip()
        res = {}
        # 0: reading key
        # 1: reading value
        mode = 0
        buff = 0
        key = None
        # intial
        if text.startswith(self.prefix):
            mode = 0
            buff = buff + len(self.prefix)
        else:
            return "E"

        while buff < len(text):
            if mode == 0:
                m = re.search(f"(.*?){self.suffix}", text[buff:])
                if m:
                    mode = 1
                    buff = buff + m.end()
                    key = m.group(1)
                else:
                    print(res)
                    return None
            elif mode == 1:
                m = re.search(f"(.*?){self.prefix}",
                              text[buff:], flags=re.DOTALL)
                mode = 0
                if m:
                    res[key] = m.group(1).strip()
                    buff = buff + m.end()
                else:
                    res[key] = text[buff:].strip()
                    buff = len(text)
                key = None

        return res
