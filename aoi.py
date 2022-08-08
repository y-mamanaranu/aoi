import discord
import asyncio
from logging import getLogger, INFO, DEBUG, StreamHandler
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
                 get_status,
                 get_channel_id,
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

# Crate object to connect Discord
intents = discord.Intents.default()
intents.reactions = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    """Run at activated.

    Notify to terminal when Aoi is activated.
    """
    print("Aoi is started")


@client.event
async def on_message(message):
    """Run on message is sent.

    Excute commands in Discord.
    `;roles`: List name and id of roles.
    `;text_channels`: List name and id of text channels.
    `;guild`: Return name and id of guild.
    `;setprefix <prefix>`: Change prefix to `prefix`. Default prefix is `;`.
    `;setchannel <channel_id>`: Change ID of channel to monitor to `channel_id`. Default is `None`.
    `;setrole <role_id>`: Change ID of role to assign to `role_id`. Default is `None`.
    `;setadmin <admin_role_id>`: Change ID of admin role to `admin_role_id`. Default is `None`.
    `;eliminate`: Elminate message from leaved member in channel to monitor.
    """
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    GUILD_ID = message.guild.id
    PREFIX = get_prefix(DATABASE_URL, GUILD_ID)

    # ;help
    if message.content == f"{PREFIX}help":
        await message.channel.send("""`;help`: Show help.
`;status`: Show current config.
`;roles`: List name and id of roles.
`;text_channels`: List name and id of text channels.
`;guild`: Return name and id of guild.
`;setprefix <prefix>`: Change prefix to `prefix`. Default prefix is `;`.
`;setchannel <channel_id>`: Change ID of channel to monitor to `channel_id`. Default is `None`.
`;setrole <role_id>`: Change ID of role to assign to `role_id`. Default is `None`.
`;setadmin <admin_role_id>`: Change ID of admin role to `admin_role_id`. Default is `None`.""")
        return

    # ;status
    if message.content == f"{PREFIX}status":
        CHANNEL_ID, ROLE_ID, ADMIN_ROLE_ID, PREFIX = get_status(DATABASE_URL,
                                                                GUILD_ID)
        if CHANNEL_ID is not None:
            CHANNEL_ID = get(message.guild.channels, id=CHANNEL_ID)
        if ROLE_ID is not None:
            ROLE_ID = get(message.guild.roles, id=ROLE_ID)
        if ADMIN_ROLE_ID is not None:
            ADMIN_ROLE_ID = get(message.guild.roles, id=ADMIN_ROLE_ID)
        await message.channel.send(f"""Prefix is {PREFIX}.
ID of channel to monitor is {CHANNEL_ID}.
ID of role to assign is {ROLE_ID}.
ID of admin role is {ADMIN_ROLE_ID}.""")
        return

    # ;roles
    if message.content == f"{PREFIX}roles":
        if not await check_privilage(DATABASE_URL, GUILD_ID, message):
            return

        text = []
        for role in message.guild.roles:
            text.append(f"{role.name}: {role.id}")
        await message.channel.send("\n".join(text))
        return

    # ;text_channels
    if message.content == f"{PREFIX}text_channels":
        if not await check_privilage(DATABASE_URL, GUILD_ID, message):
            return

        text = []
        for chann in message.guild.text_channels:
            text.append(f"{chann.name}: {chann.id}")
        await message.channel.send("\n".join(text))
        return

    # ;guild
    if message.content == f"{PREFIX}guild":
        if not await check_privilage(DATABASE_URL, GUILD_ID, message):
            return

        await message.channel.send(f"{message.guild.name}: {message.guild.id}")
        return

    # ;setprefix <prefix>
    if message.content.startswith(f"{PREFIX}setprefix "):
        if not await check_privilage(DATABASE_URL, GUILD_ID, message):
            return

        res = message.content.split(" ")
        if len(res) == 1:
            await message.channel.send(f"Need argument <prefix>.")
        elif len(res) == 2:
            PREFIX = res[1]
            update_prefix(DATABASE_URL, GUILD_ID, PREFIX)
            await message.channel.send(f"Prefix is changed to {PREFIX}.")
        else:
            await message.channel.send(f"Argument <prefix> contains extra spaces.")
        return

    # ;setchannel <channel_id>
    if message.content.startswith(f"{PREFIX}setchannel "):
        if not await check_privilage(DATABASE_URL, GUILD_ID, message):
            return

        res = message.content.split(" ")
        if len(res) == 1:
            await message.channel.send(f"Need argument <channel_id>.")
        elif len(res) == 2:
            CHANNEL_ID = res[1]
            if not CHANNEL_ID.isnumeric():
                await message.channel.send(f"Argument <channel_id> must be interger.")
            else:
                CHANNEL_ID = int(CHANNEL_ID)
                channel = get(message.guild.text_channels, id=CHANNEL_ID)
                if channel is None:
                    await message.channel.send(f"Channel with ID of {CHANNEL_ID} does not exist.")
                else:
                    update_channel_id(DATABASE_URL, GUILD_ID, CHANNEL_ID)
                    await message.channel.send(f"Channel to monitor is changed to {channel}.")
        else:
            await message.channel.send(f"Argument <channel_id> contains extra spaces.")
        return

    # ;setrole <role_id>
    if message.content.startswith(f"{PREFIX}setrole "):
        if not await check_privilage(DATABASE_URL, GUILD_ID, message):
            return

        res = message.content.split(" ")
        if len(res) == 1:
            await message.channel.send(f"Need argument <role_id>.")
        elif len(res) == 2:
            ROLE_ID = res[1]
            if not ROLE_ID.isnumeric():
                await message.channel.send(f"Argument <role_id> must be interger.")
            else:
                ROLE_ID = int(ROLE_ID)
                role = get(message.author.roles, id=ROLE_ID)
                if role is None:
                    await message.channel.send(f"Argument <role_id> must be ID of role you have.")
                else:
                    update_role_id(DATABASE_URL, GUILD_ID, ROLE_ID)
                    await message.channel.send(f"Role to assign is changed to {role}.")
        else:
            await message.channel.send(f"Argument <role_id> contains extra spaces.")
        return

    # ;setadmin <admin_role_id>
    if message.content.startswith(f"{PREFIX}setadmin "):
        if not await check_privilage(DATABASE_URL, GUILD_ID, message):
            return

        res = message.content.split(" ")
        if len(res) == 1:
            await message.channel.send(f"Need argument <admin_role_id>.")
        elif len(res) == 2:
            ADMIN_ROLE_ID = res[1]
            if not ADMIN_ROLE_ID.isnumeric():
                await message.channel.send(f"Argument <admin_role_id> must be interger.")
            else:
                ADMIN_ROLE_ID = int(ADMIN_ROLE_ID)
                admin_role = get(message.author.roles, id=ADMIN_ROLE_ID)
                if admin_role is None:
                    await message.channel.send(f"Argument <admin_role_id> must be ID of role you have.")
                else:
                    update_admin_role_id(DATABASE_URL, GUILD_ID, ADMIN_ROLE_ID)
                    await message.channel.send(f"Admin role is changed to {admin_role}.")
        else:
            await message.channel.send(f"Argument <admin_role_id> contains extra spaces.")
        return

    # ;eliminate
    if message.content == f"{PREFIX}eliminate":
        if not await check_privilage(DATABASE_URL, GUILD_ID, message):
            return

        member_cand = ["Message from user following will be eliminated."]
        message_cand = []
        CHANNEL_ID = get_channel_id(DATABASE_URL, GUILD_ID)
        if CHANNEL_ID is not None:
            channel = client.get_channel(CHANNEL_ID)
            async for m in channel.history(limit=200):
                # skip if author is bot
                if m.author.bot:
                    continue

                # check if author is member
                res = await m.guild.query_members(user_ids=[m.author.id])
                if len(res) == 0:
                    member_cand.append(f"<@{m.author.id}>")
                    message_cand.append(m)

            if len(member_cand) > 1:
                confirm_content = f"YES, eliminate in {message.guild}."
                member_cand.append(
                    f"If you want to excute elimination, plese type `{confirm_content}`.")
                await message.channel.send("\n".join(member_cand))

                def check(m):
                    """Check if it's the same user and channel."""
                    return m.author == message.author and m.channel == message.channel

                try:
                    response = await client.wait_for('message', check=check, timeout=30.0)
                except asyncio.TimeoutError:
                    await message.channel.send("Elimination is canceled with timeout.")
                    return

                if response.content == confirm_content:
                    for m in message_cand:
                        await m.delete()
                    await message.channel.send("Elimination is excuted.")
                    return
                else:
                    await message.channel.send("Elimination is canceled.")
                    return

            else:
                await message.channel.send("No message to eliminate is found.")
                return
        else:
            await message.channel.send(f"ID of channel to monitor is not set.")
            return


@ client.event
async def on_raw_reaction_add(payload):
    """Run on reaction is made.

    When a member with `ROLE` reacts on `CHANNEL`, `ROLE` is given to the person who sent the message.
    """
    logger.debug(f"start on_raw_reaction_add")

    GUILD_ID = payload.guild_id
    logger.debug(f"GUILD_ID: {GUILD_ID}")
    CHANNEL_ID, ROLE_ID, _ = get_ids(DATABASE_URL, GUILD_ID)
    logger.debug(f"CHANNEL_ID: {CHANNEL_ID}")
    logger.debug(f"ROLE_ID: {ROLE_ID}")
    if None not in (CHANNEL_ID, ROLE_ID) and payload.channel_id == CHANNEL_ID:
        ROLE = get(payload.member.roles, id=ROLE_ID)
        logger.debug(f"ROLE: {ROLE}")
        if ROLE is not None:
            channel = client.get_channel(CHANNEL_ID)
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

    logger.debug(f"end on_raw_reaction_add")
client.run(TOKEN)
