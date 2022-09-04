from discord.ext import commands
from discord.ext import tasks
import datetime
import discord
import io
from discord import app_commands
from discord.app_commands import locale_str as _T
from . import update_tenki_id, get_database_url, convert_channel_to_mention, get_all_tenki_id

from selenium import webdriver
from selenium.webdriver.common.by import By

DATABASE_URL = get_database_url()

JST = datetime.timezone(datetime.timedelta(hours=9), name='JST')


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


def get_image():
    """"""
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=800,1000")
    driver = webdriver.Chrome('chromedriver', options=options)
    driver.implicitly_wait(10)

    url = "https://tenki.jp"
    driver.get(url)
    img = driver.find_element(By.ID, "forecast-map-wrap").screenshot_as_png

    f = io.BytesIO(img)
    f.name = "tenki.png"
    return discord.File(f)


class Tenki_JP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(hours=24)
    async def post_tenki(self):
        """"""
        image = get_image()
        embed = discord.Embed()
        embed.set_author(name="tenki.jp",
                         url="https://tenki.jp",
                         icon_url="http://static.tenki.jp/images/icon/logo/icon_tenkijp_640_640.png")

        for tenki_id, in get_all_tenki_id(DATABASE_URL):
            tenki = self.bot.get_channel(tenki_id)
            if tenki is None:
                continue
            await tenki.send(file=image, embed=embed)

    @app_commands.command()
    async def tenki(self, interaction: discord.Interaction):
        """Post weather forecast of tenki.jp."""
        await interaction.response.defer()
        image = get_image()

        embed = discord.Embed()
        embed.set_author(name="tenki.jp",
                         url="https://tenki.jp",
                         icon_url="http://static.tenki.jp/images/icon/logo/icon_tenkijp_640_640.png")
        await interaction.followup.send(file=image, embed=embed)

    @app_commands.command()
    @app_commands.describe(tenki=_T('Weather forecast channel: empty for disable.'))
    async def settenki(self, interaction: discord.Integration, tenki: discord.TextChannel = None):
        """Change #Tenki.

        Previlage of administrator is required.
        """
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Previlage of administrator is required.")
            return

        GUILD_ID = interaction.guild_id

        if tenki is None:
            update_tenki_id(DATABASE_URL, GUILD_ID, tenki)
            await interaction.response.send_message("#Tenki is changed "
                                                    f"to {tenki}.")
        else:
            update_tenki_id(DATABASE_URL, GUILD_ID, tenki.id)
            await interaction.response.send_message("#Tenki is changed "
                                                    f"to {convert_channel_to_mention(tenki.id)}.")
        return


async def setup(bot):
    await bot.add_cog(Tenki_JP(bot))
