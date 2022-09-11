from discord import app_commands
from pathlib import Path
from typing import Optional
import discord
import gettext
import logging

_log = logging.getLogger(__name__)


def get_LANG(locale: str):
    return gettext.translation(domain='aoi',
                               localedir=Path(__file__).with_name("locale"),
                               languages=[locale],
                               fallback=True).gettext


class Translator(app_commands.Translator):
    # async def load(self):
    # this gets called when the translator first gets loaded!

    # async def unload(self):
    # in case you need to switch translators, this gets called when being
    # removed

    async def translate(self, string: app_commands.locale_str, locale: discord.Locale, context: app_commands.TranslationContext) -> Optional[str]:
        """
        `locale_str` is the string that is requesting to be translated
        `locale` is the target language to translate to
        `context` is the origin of this string, eg TranslationContext.command_name, etc
        This function must return a string (that's been translated), or `None` to signal no available translation available, and will default to the original.
        """
        message_str = string.message
        LANG = get_LANG(str(locale))
        res_str = LANG(message_str)

        return res_str
