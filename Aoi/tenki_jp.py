from discord import app_commands
from discord.app_commands import locale_str as _T
from discord.ext import commands
from discord.ext import tasks
from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
import discord
import io
from PIL import Image

from . import (
    convert_channel_to_mention,
    get_database_url,
    help_command,
)
from .database import (
    get_all_tenki_id,
    update_tenki_id,
)

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


async def get_image(interaction: discord.Interaction = None,
                    select: bool = False,
                    week: bool = False):
    """"""
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-dev-shm-usage")
    if not week:
        options.add_argument("--window-size=800,1000")
    else:
        options.add_argument("--window-size=700,2200")
    driver = webdriver.Chrome('chromedriver', options=options)

    if not week:
        url = "https://tenki.jp"
        driver.get(url)

        if select and interaction:
            res = driver.find_element(By.ID,
                                      "forecast-public-date-entries").find_elements(By.TAG_NAME, "a")

            class HogeList(discord.ui.View):
                def __init__(self, args: list):
                    super().__init__()
                    self.add_item(HugaList(args))

            class HugaList(discord.ui.Select):
                def __init__(self, args):
                    self.args = args
                    options = []
                    for item in args:
                        options.append(
                            discord.SelectOption(
                                label=item, description=''))

                    super().__init__(placeholder='', min_values=1, max_values=1, options=options)

                async def callback(self, interaction: discord.Interaction):
                    i = self.args.index(self.values[0])
                    driver.execute_script('arguments[0].click();', res[i])
                    img = driver.find_element(By.ID,
                                              "forecast-map-wrap").screenshot_as_png
                    fp = io.BytesIO(img)
                    fp.name = "tenki.png"
                    image = discord.File(fp)

                    embed = discord.Embed()
                    embed.set_author(name="tenki.jp",
                                     url="https://tenki.jp",
                                     icon_url="http://static.tenki.jp/images/icon/logo/icon_tenkijp_640_640.png")
                    await interaction.response.send_message(file=image, embed=embed)

            await interaction.followup.send(view=HogeList([val.text for val in res]))
            return
        else:
            img = driver.find_element(By.ID,
                                      "forecast-map-wrap").screenshot_as_png
            fp = io.BytesIO(img)
    else:
        url = "https://tenki.jp/week"
        driver.get(url)

        res = driver.find_elements(By.CLASS_NAME, "week-thisweek-table")
        img0 = Image.open(io.BytesIO(res[0].screenshot_as_png))
        img1 = Image.open(io.BytesIO(res[1].screenshot_as_png))

        img = Image.new('RGB', (max(img0.width, img1.width),
                        img0.height + img1.height))
        img.paste(img0, (0, 0))
        img.paste(img1, (0, img0.height))

        fp = io.BytesIO()
        img.save(fp, format="png")
        fp.seek(0)

    fp.name = "tenki.png"
    image = discord.File(fp)
    if interaction is None:
        return image
    else:
        embed = discord.Embed()
        embed.set_author(name="tenki.jp",
                         url="https://tenki.jp",
                         icon_url="http://static.tenki.jp/images/icon/logo/icon_tenkijp_640_640.png")
        await interaction.followup.send(file=image, embed=embed)


class Tenki_JP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(hours=24)
    async def post_tenki(self):
        """"""
        image = await get_image()
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
    @help_command()
    async def tenki(self,
                    interaction: discord.Interaction,
                    select: bool = False,
                    week: bool = False,
                    help: bool = False):
        """Post weather forecast of tenki.jp.

        Parameters
        ----------
        interaction : discord.Interaction
            _description_
        select : bool, optional
            Wheter to select day to show, by default False
        week : bool, optional
            Wheter to show weekly forecast instead, by default False
        help : bool, optional
            Wether to show help instead, by default False
        """
        await interaction.response.defer()
        await get_image(interaction=interaction,
                        select=select,
                        week=week)

    @app_commands.command()
    @app_commands.describe(tenki=_T('Weather forecast channel, empty for disable.'))
    @help_command()
    async def settenki(self,
                       interaction: discord.Interaction,
                       tenki: discord.TextChannel = None,
                       help: bool = False):
        """Change #Tenki.

        Previlage of administrator is required.

        Parameters
        ----------
        interaction : discord.Interaction
            _description_
        tenki : discord.TextChannel, optional
            Channel to set as #Tenki, by default None
            #Tenki is weather forecast channel.
            If #Tenki is not None, post wheter forecat of tenki.jp to #Tenki on 5:00 JST.
        help : bool, optional
            Wether to show help instead, by default False
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
