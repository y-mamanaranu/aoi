import imp
import os
import re
import pydoc
import inspect
from functools import wraps
import discord


def help_command():
    def _help_command(func):
        params = inspect.signature(func).parameters
        i = list(params.keys()).index("interaction")

        @wraps(func)
        async def wrapper(*args, **kwargs):
            if kwargs.get("help"):
                interaction: discord.Interaction = args[i]
                help = pydoc.render_doc(func)
                await interaction.response.send_message(help)
            else:
                return await func(*args, **kwargs)
        return wrapper
    return _help_command


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
