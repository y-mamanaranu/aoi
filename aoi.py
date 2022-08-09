"""Aoi Bot code."""
from discord.ext import commands
import discord
import asyncio
from discord.ext.commands import Context, DefaultHelpCommand
from logging import getLogger, INFO, StreamHandler
# from logging import DEBUG
from discord.utils import get
from Aoi import (get_token,
                 get_database_url,
                 init_db,
                 get_ids,
                 get_prefix,
                 update_channel_id,
                 update_prefix,
                 update_role_id,
                 update_admin_role_id,
                 convert_user_to_mention,
                 convert_channel_to_mention,
                 convert_role_to_mention,
                 get_status,
                 get_channel_id,
                 remove_ids,
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
    """Show current config."""
    GUILD_ID = ctx.guild.id

    CHANNEL_ID, ROLE_ID, ADMIN_ROLE_ID, PREFIX = get_status(DATABASE_URL,
                                                            GUILD_ID)
    await ctx.channel.send(f"""Prefix is {PREFIX}.
ID of profile channel is {convert_channel_to_mention(CHANNEL_ID)}.
ID of role to assign is {convert_role_to_mention(ROLE_ID)}.
ID of admin role is {convert_role_to_mention(ADMIN_ROLE_ID)}.""")
    return


@bot.command()
async def roles(ctx: Context):
    """List roles."""
    GUILD_ID = ctx.guild.id

    if not await check_privilage(DATABASE_URL, GUILD_ID, ctx.message):
        return

    text = []
    for role in ctx.guild.roles:
        text.append(f"{convert_role_to_mention(role.id)}")
    await ctx.channel.send("\n".join(text))
    return


@bot.command()
async def text_channels(ctx: Context):
    """List text channels."""
    GUILD_ID = ctx.guild.id

    if not await check_privilage(DATABASE_URL, GUILD_ID, ctx.message):
        return

    text = []
    for chann in ctx.guild.text_channels:
        text.append(f"{convert_channel_to_mention(chann.id)}")
    await ctx.channel.send("\n".join(text))
    return


@bot.command()
async def members(ctx: Context):
    """List members."""
    GUILD_ID = ctx.guild.id

    if not await check_privilage(DATABASE_URL, GUILD_ID, ctx.message):
        return

    text = []
    for member in ctx.guild.members:
        if member.bot:
            continue

        text.append(f"{convert_user_to_mention(member.id)}")
    await ctx.channel.send("\n".join(text))
    return


@bot.command()
async def bots(ctx: Context):
    """List of bots."""
    GUILD_ID = ctx.guild.id

    if not await check_privilage(DATABASE_URL, GUILD_ID, ctx.message):
        return

    text = []
    for member in ctx.guild.members:
        if not member.bot:
            continue

        text.append(f"{convert_user_to_mention(member.id)}")
    await ctx.channel.send("\n".join(text))
    return


@bot.command()
async def guild(ctx: Context):
    """Return name and id of guild."""
    GUILD_ID = ctx.guild.id

    if not await check_privilage(DATABASE_URL, GUILD_ID, ctx.message):
        return

    await ctx.channel.send(f"{ctx.guild.name}: {ctx.guild.id}")
    return


@bot.command()
async def setprefix(ctx: Context, prefix: str):
    """Change prefix.

    Default prefix is `;`.
    """
    GUILD_ID = ctx.guild.id

    if not await check_privilage(DATABASE_URL, GUILD_ID, ctx.message):
        return

    update_prefix(DATABASE_URL, GUILD_ID, prefix)
    await ctx.channel.send(f"Prefix is changed to `{prefix}`.")
    return


@bot.command()
async def setchannel(ctx: Context, channel_id: str):
    """Change ID of profile channel.

    Default profile channel is `None`.
    """
    GUILD_ID = ctx.guild.id
    channel_id = convert_mention_to_channel(channel_id)

    if not await check_privilage(DATABASE_URL, GUILD_ID, ctx.message):
        return

    if not channel_id.isnumeric():
        await ctx.channel.send("Argument `<channel_id>` must be interger.")
    else:
        channel_id = int(channel_id)
        channel = get(ctx.guild.text_channels, id=channel_id)
        if channel is None:
            await ctx.channel.send(f"Channel with ID of {channel_id} does not exist.")
        else:
            update_channel_id(DATABASE_URL, GUILD_ID, channel_id)
            await ctx.channel.send("Profile channel is changed "
                                   f"to {convert_channel_to_mention(channel_id)}.")
    return


@bot.command()
async def setrole(ctx: Context, role_id: str):
    """Change ID of role to assign.

    Default role to assign is `None`.
    """
    GUILD_ID = ctx.guild.id
    role_id = convert_mention_to_role(role_id)

    if not await check_privilage(DATABASE_URL, GUILD_ID, ctx.message):
        return

    if not role_id.isnumeric():
        await ctx.channel.send("Argument `<role_id>` must be interger.")
    else:
        role_id = int(role_id)
        role = get(ctx.author.roles, id=role_id)
        if role is None:
            await ctx.channel.send("Argument `<role_id>` must be ID of role you have.")
        else:
            update_role_id(DATABASE_URL, GUILD_ID, role_id)
            await ctx.channel.send("Role to assign is changed "
                                   f"to {convert_role_to_mention(role_id)}.")
    return


@bot.command()
async def setadmin(ctx: Context, admin_role_id: str):
    """Change ID of admin role.

    Default admin role is `None`.
    """
    GUILD_ID = ctx.guild.id
    admin_role_id = convert_mention_to_role(admin_role_id)

    if not await check_privilage(DATABASE_URL, GUILD_ID, ctx.message):
        return

    if not admin_role_id.isnumeric():
        await ctx.channel.send("Argument `<admin_role_id>` must be interger.")
    else:
        admin_role_id = int(admin_role_id)
        admin_role = get(ctx.author.roles, id=admin_role_id)
        if admin_role is None:
            await ctx.channel.send("Argument `<admin_role_id>` must be ID of role you have.")
        else:
            update_admin_role_id(DATABASE_URL, GUILD_ID, admin_role_id)
            await ctx.channel.send("Admin role is changed "
                                   f"to {convert_role_to_mention(admin_role_id)}.")
    return


@bot.command()
async def eliminate(ctx: Context):
    """Elminate message from leaved member in profile channel."""
    GUILD_ID = ctx.guild.id

    if not await check_privilage(DATABASE_URL, GUILD_ID, ctx.message):
        return

    member_cand = ["Message from user following will be eliminated."]
    message_cand = []
    CHANNEL_ID = get_channel_id(DATABASE_URL, GUILD_ID)
    if CHANNEL_ID is not None:
        channel = bot.get_channel(CHANNEL_ID)
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
        await ctx.channel.send("ID of profile channel is not set.")
        return


@bot.command()
async def adjust(ctx: Context):
    """Delete message from duplicate member in profile channel."""
    GUILD_ID = ctx.guild.id

    if not await check_privilage(DATABASE_URL, GUILD_ID, ctx.message):
        return

    memberlist = []
    message_cand = []
    CHANNEL_ID = get_channel_id(DATABASE_URL, GUILD_ID)
    if CHANNEL_ID is not None:
        channel = bot.get_channel(CHANNEL_ID)
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
        await ctx.channel.send("ID of profile channel is not set.")
        return


@bot.command()
async def profile(ctx: Context, user_id: str):
    """Show profile of member."""
    GUILD_ID = ctx.guild.id
    user_id = convert_mention_to_user(user_id)

    # If CHANNEL_ID is None, stop
    CHANNEL_ID = get_channel_id(DATABASE_URL, GUILD_ID)
    if CHANNEL_ID is None:
        await ctx.channel.send("ID of profile channel is not set.")
        return

    # If user_id is invalid, stop
    res = await ctx.guild.query_members(user_ids=[user_id])
    if len(res) == 0:
        await ctx.channel.send("Invalid `user_id`.")
        return
    else:
        member, = res

    # Show profile
    channel = bot.get_channel(CHANNEL_ID)

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


@ bot.event
async def on_raw_reaction_add(payload):
    """Run on reaction is made.

    When a member with `ROLE` reacts on `CHANNEL`,
    `ROLE` is given to the person who sent the message.
    """
    logger.debug("start on_raw_reaction_add")

    GUILD_ID = payload.guild_id
    logger.debug(f"GUILD_ID: {GUILD_ID}")
    CHANNEL_ID, ROLE_ID, _ = get_ids(DATABASE_URL, GUILD_ID)
    logger.debug(f"CHANNEL_ID: {CHANNEL_ID}")
    logger.debug(f"ROLE_ID: {ROLE_ID}")
    if None not in (CHANNEL_ID, ROLE_ID) and payload.channel_id == CHANNEL_ID:
        ROLE = get(payload.member.roles, id=ROLE_ID)
        logger.debug(f"ROLE: {ROLE}")
        if ROLE is not None:
            channel = bot.get_channel(CHANNEL_ID)
            logger.debug(f"channel: {channel}")

            message_id = payload.message_id
            logger.debug(f"message_id: {message_id}")

            message = await channel.fetch_message(message_id)
            logger.debug(f"message: {message}")

            member, = await message.guild.query_members(user_ids=[message.author.id])
            logger.debug(f"member: {member}")

            if ROLE not in member.roles:
                logger.debug(f"Add {ROLE} to {member}")
                await member.add_roles(ROLE)

    logger.debug("end on_raw_reaction_add")


@bot.event
async def on_guild_join(guild):
    """When the bot joins the guild."""
    insert_ids(DATABASE_URL, guild.id)


@bot.event
async def on_guild_remove(guild):
    """When the bot is removed from the guild."""
    remove_ids(DATABASE_URL, guild.id)


bot.run(TOKEN)
