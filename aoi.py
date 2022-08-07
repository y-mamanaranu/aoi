import discord
from logging import getLogger, INFO, DEBUG, StreamHandler
from discord.utils import get
from Aoi import get_token, get_database_url, init_db, get_ids

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
    print('Aoi is started')


@client.event
async def on_message(message):
    """Run on message is sent.

    Implement commands in Discord.
    `;roles`: List name and id of roles.
    `;text_channels`: List name and id of text channels.
    `;guild`: Return name and id of guild.
    """
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    # 「;roles」と発言したらロールの名前とID一覧が返る
    if message.content == ';roles':
        text = []
        for role in message.guild.roles:
            text.append(f"{role.name}: {role.id}")
        await message.channel.send("\n".join(text))
    # 「;text_channels」と発言したらロールの名前とID一覧が返る
    elif message.content == ';text_channels':
        text = []
        for chann in message.guild.text_channels:
            text.append(f"{chann.name}: {chann.id}")
        await message.channel.send("\n".join(text))
    elif message.content == ";guild":
        await message.channel.send(f"{message.guild.name}: {message.guild.id}")


@client.event
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
            channel_id = payload.channel_id
            logger.debug(f"channel_id: {channel_id}")

            channel = client.get_channel(channel_id)
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
