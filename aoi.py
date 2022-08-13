"""Aoi Bot code."""
from discord.ext import commands
import discord
import random
import asyncio
from discord.ext.commands import Context, DefaultHelpCommand
from logging import getLogger, INFO, StreamHandler
# from logging import DEBUG
from discord.utils import get
from Aoi import (get_token,
                 get_database_url,
                 init_db,
                 get_prefix,
                 update_profile_id,
                 update_prefix,
                 update_freshman_id,
                 update_admin_id,
                 convert_user_to_mention,
                 convert_channel_to_mention,
                 convert_role_to_mention,
                 get_pre_pro_log_fre_sen_adm,
                 get_pro_log_fre_sen,
                 update_log_id,
                 update_senior_id,
                 remove_ids,
                 get_profile_id,
                 convert_mention_to_channel,
                 convert_mention_to_role,
                 convert_mention_to_user,
                 insert_ids,
                 check_privilage)

# Setup logging
logger_level = INFO
# logger_level = DEBUG
logger = getLogger(__name__)
logger.setLevel(logger_level)

ch = StreamHandler()
ch.setLevel(logger_level)
logger.addHandler(ch)

# Get envriomental variables.
TOKEN = get_token()
DATABASE_URL = get_database_url()

# Initialize Heroku Postgres
init_db(DATABASE_URL)


def get_prefix_ctx(client, message):
    """Get prefix in context."""
    GUILD_ID = message.guild.id
    PREFIX = get_prefix(DATABASE_URL, GUILD_ID)
    return PREFIX


def get_message(client, message):
    """Get prefix in context."""
    return str(message)


# Crate object to connect Discord
intents = discord.Intents.default()
intents.reactions = True
intents.members = True
# client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix=(get_prefix_ctx),
                   help_command=DefaultHelpCommand(indent=0,
                   no_category="Commands"),
                   intents=intents)


@bot.event
async def on_ready():
    """Run at activated.

    Notify to terminal when Aoi is activated.
    """
    print("Aoi is started")
    await bot.change_presence(activity=discord.Game(name=";help"))


@bot.command()
async def status(ctx: Context):
    """Show current config.

    Prefix is Prefix of command.
    #Profile is Profile channel.
    #Log is Log channel.
    @Freshman is Role to assign to new member.
    @Senior is Role who can assign to new member.
    @Admin is Role who can use config commands.

    設定を表示します。

    PrefixはコマンドのPrefixです。
    #Profileは自己紹介のチャンネルです。
    #Logはログを出力するチャンネルです。
    @Freshmanは新規に付与するロールです。
    @Seniorは新規への付与を許可するロールです。
    @Adminは設定の変更を許可するロールです。
    """
    GUILD_ID = ctx.guild.id

    PREFIX, PROFILE_ID, LOG_ID, FRESHMAN_ID, SENIOR_ID, ADMIN_ID = \
        get_pre_pro_log_fre_sen_adm(DATABASE_URL,
                                    GUILD_ID)
    await ctx.channel.send(f"""Prefix is `{PREFIX}`.
#Profile is {convert_channel_to_mention(PROFILE_ID)}.
#Log is {convert_channel_to_mention(LOG_ID)}.
@Freshman is {convert_role_to_mention(FRESHMAN_ID)}.
@Senior is {convert_role_to_mention(SENIOR_ID)}.
@Admin is {convert_role_to_mention(ADMIN_ID)}.""")
    return


@bot.command()
async def roles(ctx: Context):
    """List roles.

    ロールの一覧を出力します。
    """
    text = []
    for role in ctx.guild.roles:
        text.append(f"{convert_role_to_mention(role.id)}")
    await ctx.channel.send("\n".join(text))
    return


@bot.command()
async def text_channels(ctx: Context):
    """List text channels.

    テキストチャンネルの一覧を出力します。
    """
    text = []
    for chann in ctx.guild.text_channels:
        text.append(f"{convert_channel_to_mention(chann.id)}: {chann.id}")
    await ctx.channel.send("\n".join(text))
    return


@bot.command()
async def voice_channels(ctx: Context):
    """List voice channels.

    ボイスチャンネルの一覧を出力します。
    """
    text = []
    for chann in ctx.guild.voice_channels:
        text.append(f"{convert_channel_to_mention(chann.id)}: {chann.id}")
    await ctx.channel.send("\n".join(text))
    return


@bot.command()
async def members(ctx: Context):
    """List members.

    メンバーの一覧を出力します。
    """
    text = []
    for member in ctx.guild.members:
        if member.bot:
            continue

        text.append(f"{convert_user_to_mention(member.id)}")
    await ctx.channel.send("\n".join(text))
    return


@bot.command()
async def bots(ctx: Context):
    """List bots.

    ボットの一覧を出力します。
    """
    text = []
    for member in ctx.guild.members:
        if not member.bot:
            continue

        text.append(f"{convert_user_to_mention(member.id)}")
    await ctx.channel.send("\n".join(text))
    return


@bot.command()
async def guild(ctx: Context):
    """Return name and id of guild.

    @Admin is required excute this commnad.

    サーバーの名前とIDを返します。

    実行するには@Adminが必要です。
    """
    GUILD_ID = ctx.guild.id

    if not await check_privilage(DATABASE_URL, GUILD_ID, ctx.message):
        return

    await ctx.channel.send(f"{ctx.guild.name}: {ctx.guild.id}")
    return


@bot.command()
async def setprefix(ctx: Context, prefix: str):
    """Change prefix to `prefix`.

    Prefix is Prefix of command.
    Default prefix is `;`.

    Prefixを`prefix`に変更します。

    PrefixはコマンドのPrefixです。
    デフォルトのPrefixは`;`です。
    """
    GUILD_ID = ctx.guild.id

    if not await check_privilage(DATABASE_URL, GUILD_ID, ctx.message):
        return

    prefix = str(prefix)
    update_prefix(DATABASE_URL, GUILD_ID, prefix)
    await ctx.channel.send(f"Prefix is changed to `{prefix}`.")
    return


@bot.command()
async def setprofile(ctx: Context, profile_id: str):
    """Change ID of #Profile to `profile_id`.

    @Admin is required excute this commnad.
    #Profile is Profile channel.
    Default ID of #Profile is `None`.

    #ProfileのIDを`profile_id`に変更します。

    実行するには@Adminが必要です。
    #Profileは自己紹介のチャンネルです。
    デフォルトの#ProfileのIDは`None`です。
    """
    GUILD_ID = ctx.guild.id
    profile_id = convert_mention_to_channel(profile_id)

    if not await check_privilage(DATABASE_URL, GUILD_ID, ctx.message):
        return

    if profile_id == "None":
        profile_id = None
        update_profile_id(DATABASE_URL, GUILD_ID, profile_id)
        await ctx.channel.send("#Profile is changed "
                               f"to {profile_id}.")
    elif not profile_id.isnumeric():
        await ctx.channel.send("Argument `<profile_id>` must be interger.")
    else:
        profile_id = int(profile_id)
        channel = get(ctx.guild.text_channels, id=profile_id)
        if channel is None:
            await ctx.channel.send(f"Channel with ID of {profile_id} does not exist.")
        else:
            update_profile_id(DATABASE_URL, GUILD_ID, profile_id)
            await ctx.channel.send("#Profile is changed "
                                   f"to {convert_channel_to_mention(profile_id)}.")
    return


@bot.command()
async def setlog(ctx: Context, log_id: str):
    """Change ID of #Log to `log_id`.

    @Admin is required excute this commnad.
    #Log is Log channel.
    Default ID of #Log is `None`.

    #LogのIDを`log_id`に変更します。

    実行するには@Adminが必要です。
    #Logはログを出力するチャンネルです。
    デフォルトの#LogのIDは`None`です。
    """
    GUILD_ID = ctx.guild.id
    log_id = convert_mention_to_channel(log_id)

    if not await check_privilage(DATABASE_URL, GUILD_ID, ctx.message):
        return

    if log_id == "None":
        log_id = None
        update_log_id(DATABASE_URL, GUILD_ID, log_id)
        await ctx.channel.send("#Log is changed "
                               f"to {log_id}.")
    elif not log_id.isnumeric():
        await ctx.channel.send("Argument `<log_id>` must be interger.")
    else:
        log_id = int(log_id)
        log = get(ctx.guild.text_channels, id=log_id)
        if log is None:
            await ctx.channel.send(f"Channel with ID of {log_id} does not exist.")
        else:
            update_log_id(DATABASE_URL, GUILD_ID, log_id)
            await ctx.channel.send("#Log is changed "
                                   f"to {convert_channel_to_mention(log_id)}.")
    return


@bot.command()
async def setfreshman(ctx: Context, freshman_id: str):
    """Change ID of @Freshman to `freshman_id`.

    @Admin is required excute this commnad.
    @Freshman is Role to assign to new member.
    Default ID of @Freshman is `None`.

    @FreshmanのIDを`freshman_id`に変更します。

    実行するには@Adminが必要です。
    @Freshmanは新規に付与するロールです。
    デフォルトの@FreshmanのIDは`None`です。
    """
    GUILD_ID = ctx.guild.id
    freshman_id = convert_mention_to_role(freshman_id)

    if not await check_privilage(DATABASE_URL, GUILD_ID, ctx.message):
        return

    if freshman_id == "None":
        freshman_id = None
        update_freshman_id(DATABASE_URL, GUILD_ID, freshman_id)
        await ctx.channel.send("@Freshman is changed "
                               f"to {freshman_id}.")
    elif not freshman_id.isnumeric():
        await ctx.channel.send("Argument `<freshman_id>` must be interger.")
    else:
        freshman_id = int(freshman_id)
        role = get(ctx.author.roles, id=freshman_id)
        if role is None:
            await ctx.channel.send("Argument `<freshman_id>` must be ID of role you have.")
        else:
            update_freshman_id(DATABASE_URL, GUILD_ID, freshman_id)
            await ctx.channel.send("@Freshman is changed "
                                   f"to {convert_role_to_mention(freshman_id)}.")
    return


@bot.command()
async def setsenior(ctx: Context, senior_id: str):
    """Change ID of @Senior to `senior_id`.

    @Admin is required excute this commnad.
    @Senior is Role to assign to new member.
    Default ID of @Senior is `None`.

    @SeniorのIDを`senior_id`に変更します。

    実行するには@Adminが必要です。
    @Seniorは新規への付与を許可するロールです。
    デフォルトの@SeniorのIDは`None`です。
    """
    GUILD_ID = ctx.guild.id
    senior_id = convert_mention_to_role(senior_id)

    if not await check_privilage(DATABASE_URL, GUILD_ID, ctx.message):
        return

    if senior_id == "None":
        senior_id = None
        update_senior_id(DATABASE_URL, GUILD_ID, senior_id)
        await ctx.channel.send("@Senior is changed "
                               f"to {senior_id}.")
    elif not senior_id.isnumeric():
        await ctx.channel.send("Argument `<senior_id>` must be interger.")
    else:
        senior_id = int(senior_id)
        role = get(ctx.author.roles, id=senior_id)
        if role is None:
            await ctx.channel.send("Argument `<senior_id>` must be ID of role you have.")
        else:
            update_senior_id(DATABASE_URL, GUILD_ID, senior_id)
            await ctx.channel.send("@Senior is changed "
                                   f"to {convert_role_to_mention(senior_id)}.")
    return


@bot.command()
async def setadmin(ctx: Context, admin_id: str):
    """Change ID of @Admin to `admin_id`.

    @Admin is required excute this commnad.
    @Admin is Role who can use config commands.
    Default ID of @Admin is `None`.

    @AdminのIDを`admin_id`に変更します。

    実行するには@Adminが必要です。
    @Adminは設定の変更を許可するロールです。
    デフォルトの@AdminのIDは`None`です。
    """
    GUILD_ID = ctx.guild.id
    admin_id = convert_mention_to_role(admin_id)

    if not await check_privilage(DATABASE_URL, GUILD_ID, ctx.message):
        return

    if admin_id == "None":
        admin_id = None
        update_admin_id(DATABASE_URL, GUILD_ID, admin_id)
        await ctx.channel.send("@Admin is changed "
                               f"to {admin_id}.")
    elif not admin_id.isnumeric():
        await ctx.channel.send("Argument `<admin_id>` must be interger.")
    else:
        admin_id = int(admin_id)
        admin = get(ctx.author.roles, id=admin_id)
        if admin is None:
            await ctx.channel.send("Argument `<admin_id>` must be ID of role you have.")
        else:
            update_admin_id(DATABASE_URL, GUILD_ID, admin_id)
            await ctx.channel.send("@Admin is changed "
                                   f"to {convert_role_to_mention(admin_id)}.")
    return


@bot.command()
async def eliminate(ctx: Context):
    """Delete profile of leaved member.

    @Admin is required excute this commnad.

    居なくなったメンバーの自己紹介を削除します。

    実行するには@Adminが必要です。
    """
    GUILD_ID = ctx.guild.id

    if not await check_privilage(DATABASE_URL, GUILD_ID, ctx.message):
        return

    member_cand = ["Message from user following will be eliminated."]
    message_cand = []
    PROFILE_ID = get_profile_id(DATABASE_URL, GUILD_ID)
    if PROFILE_ID is not None:
        channel = bot.get_channel(PROFILE_ID)
        async for m in channel.history(limit=200, oldest_first=True):
            # skip if author is bot
            if m.author.bot:
                continue

            # check if author is member
            res = await m.guild.query_members(user_ids=[m.author.id])
            if len(res) == 0:
                member_cand.append(convert_user_to_mention(m.author.id))
                message_cand.append(m)

        if len(member_cand) > 1:
            confirm_content = f"YES, eliminate in {ctx.guild}."
            member_cand.append(
                f"If you want to excute elimination, plese type `{confirm_content}`.")
            await ctx.channel.send("\n".join(member_cand))

            def check(m):
                """Check if it's the same user and channel."""
                return m.author == ctx.author and m.channel == ctx.channel

            try:
                response = await bot.wait_for('message', check=check, timeout=30.0)
            except asyncio.TimeoutError:
                await ctx.channel.send("Elimination is canceled with timeout.")
                return

            if response.content == confirm_content:
                for m in message_cand:
                    await m.delete()
                await ctx.channel.send("Elimination is excuted.")
                return
            else:
                await ctx.channel.send("Elimination is canceled.")
                return

        else:
            await ctx.channel.send("No message to eliminate is found.")
            return
    else:
        await ctx.channel.send("@Profile is not set.")
        return


@bot.command()
async def adjust(ctx: Context):
    """Delete second or subsequent profile of same user.

    @Admin is required excute this commnad.

    同じユーザーの2回目以降の自己紹介を削除します。

    実行するには@Adminが必要です。
    """
    GUILD_ID = ctx.guild.id

    if not await check_privilage(DATABASE_URL, GUILD_ID, ctx.message):
        return

    memberlist = []
    message_cand = []
    PROFILE_ID = get_profile_id(DATABASE_URL, GUILD_ID)
    if PROFILE_ID is not None:
        channel = bot.get_channel(PROFILE_ID)
        async for m in channel.history(limit=200, oldest_first=True):
            # skip if author is bot
            if m.author.bot:
                continue

            # check if author is member
            if m.author.id in memberlist:
                message_cand.append(m)
            else:
                memberlist.append(m.author.id)

        if len(message_cand) > 0:
            confirm_content = f"YES, adjustment in {ctx.guild}."
            await ctx.channel.send("If you want to excute adjustment, "
                                   f"plese type `{confirm_content}`.")

            def check(m):
                """Check if it's the same user and channel."""
                return m.author == ctx.author and m.channel == ctx.channel

            try:
                response = await bot.wait_for('message', check=check, timeout=30.0)
            except asyncio.TimeoutError:
                await ctx.channel.send("Adjustment is canceled with timeout.")
                return

            if response.content == confirm_content:
                for m in message_cand:
                    await m.delete()
                await ctx.channel.send("Adjustment is excuted.")
                return
            else:
                await ctx.channel.send("Adjustment is canceled.")
                return

        else:
            await ctx.channel.send("No message to adjust is found.")
            return
    else:
        await ctx.channel.send("@Profile is not set.")
        return


@bot.command()
async def profile(ctx: Context, user_id: str):
    """Show profile of member with ID of `user_id`.

    IDが`user_id`のメンバーの自己紹介を表示します。
    """
    GUILD_ID = ctx.guild.id
    user_id = convert_mention_to_user(user_id)

    # If PROFILE_ID is None, stop
    PROFILE_ID = get_profile_id(DATABASE_URL, GUILD_ID)
    if PROFILE_ID is None:
        await ctx.channel.send("@Profile is not set.")
        return

    # If user_id is invalid, stop
    res = await ctx.guild.query_members(user_ids=[user_id])
    if len(res) == 0:
        await ctx.channel.send("Invalid `user_id`.")
        return
    else:
        member, = res

    # Show profile
    channel = bot.get_channel(PROFILE_ID)

    messages = await channel.history(limit=200, oldest_first=True).flatten()
    message = get(messages, author=member)

    if message is not None:
        embed = discord.Embed(description=message.content)
        embed.set_author(name=member.nick or member.name,
                         icon_url=member.avatar_url)

        await ctx.channel.send(embed=embed)
        return
    else:
        await ctx.channel.send("No profile is found.")
        return


@bot.command()
async def setlimit(ctx: Context, limit: str):
    """Change upper limit of voice channel which you join to `limit`.

    Value of `0` to remove limit.

    参加しているボイスチャンネルのユーザー上限を`limit`に変更します。

    値が0の場合は、上限がなくなります。
    """
    if not limit.isnumeric():
        await ctx.channel.send("Argument `<limit>` must be interger.")
    else:
        limit = int(limit)
        channel = ctx.author.voice.channel

        if channel is None:
            await ctx.channel.send("You do not join voice channel.")
            return
        else:
            await channel.edit(user_limit=limit)


@bot.command()
async def split(ctx: Context, voice_id: str):
    """Split voice channel member and move half to `voice_id`.

    ボイスチャンネルにいるメンバーを2つに分けて、半分を`voice_id`に移動します。
    """
    voice_id = convert_mention_to_channel(voice_id)
    origin = ctx.author.voice.channel

    if not voice_id.isnumeric():
        await ctx.channel.send("Argument `<voice_id>` must be interger.")
    else:
        voice_id = int(voice_id)
        channel = get(ctx.guild.voice_channels, id=voice_id)
        if channel is None:
            await ctx.channel.send(f"Channel with ID of {voice_id} does not exist.")
        else:
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
                f"> Members for {convert_channel_to_mention(channel.id)}")
            for member in members2:
                text.append(f"{convert_user_to_mention(member.id)}")
                await member.move_to(channel)

            await ctx.channel.send("\n".join(text))
    return


@bot.command()
async def splithere(ctx: Context):
    """Split voice channel member and move half here.

    ボイスチャンネルにいるメンバーを2つに分けて、半分をここに移動します。
    """
    await split(ctx, str(ctx.channel.id))


@bot.command()
async def move(ctx: Context, voice_id: str):
    """Move all voice channel member to `voice_id`.

    ボイスチャンネルにいるすべてのメンバーを`voice_id`に移動します。
    """
    voice_id = convert_mention_to_channel(voice_id)
    origin = ctx.author.voice.channel

    if not voice_id.isnumeric():
        await ctx.channel.send("Argument `<voice_id>` must be interger.")
    else:
        voice_id = int(voice_id)
        channel = get(ctx.guild.voice_channels, id=voice_id)
        if channel is None:
            await ctx.channel.send(f"Channel with ID of {voice_id} does not exist.")
        else:
            for member in origin.members:
                await member.move_to(channel)
    return


@bot.command()
async def movehere(ctx: Context):
    """Move all voice channel member here.

    ボイスチャンネルにいるすべてのメンバーをここに移動します。
    """
    await move(ctx, str(ctx.channel.id))


@ bot.event
async def on_raw_reaction_add(payload):
    """Run on reaction is made.

    When a member with `@Senior` reacts on `#Profiles`,
    `@Freshman` is given to the person who sent the message.
    """

    GUILD_ID = payload.guild_id
    PROFILE_ID, LOG_ID, FRESHMAN_ID, SENIOR_ID = get_pro_log_fre_sen(DATABASE_URL,
                                                                     GUILD_ID)
    if None in (PROFILE_ID,
                FRESHMAN_ID,
                SENIOR_ID) or payload.channel_id != PROFILE_ID:
        return

    FRESHMAN = get(payload.member.guild.roles, id=FRESHMAN_ID)
    if FRESHMAN is None:
        return

    SENIOR = get(payload.member.roles, id=SENIOR_ID)
    if SENIOR is None:
        return

    channel = bot.get_channel(PROFILE_ID)
    message_id = payload.message_id
    message = await channel.fetch_message(message_id)
    member, = await message.guild.query_members(user_ids=[message.author.id])

    if FRESHMAN in member.roles:
        return

    await member.add_roles(FRESHMAN)

    if LOG_ID is None:
        return

    channel = bot.get_channel(LOG_ID)
    await channel.send(f"{convert_user_to_mention(payload.member.id)} "
                       f"add {convert_role_to_mention(FRESHMAN_ID)} "
                       f"to {convert_user_to_mention(member.id)} via Aoi.")


@bot.event
async def on_guild_join(guild):
    """When the bot joins the guild."""
    insert_ids(DATABASE_URL, guild.id)


@bot.event
async def on_guild_remove(guild):
    """When the bot is removed from the guild."""
    remove_ids(DATABASE_URL, guild.id)


@bot.event
async def on_voice_state_update(member, before, after):
    """Run on member join or leave voice channel."""
    if member.bot:
        if before.channel is not None and before.channel.user_limit != 0:
            await before.channel.edit(user_limit=before.channel.user_limit - 1)
        if after.channel is not None and after.channel.user_limit != 0:
            await after.channel.edit(user_limit=after.channel.user_limit + 1)

bot.run(TOKEN)
