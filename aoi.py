import discord
from discord.utils import get
from Aoi import get_token, get_database_url, init_db, get_ids

# Get envriomental variables.
TOKEN = get_token()
DATABASE_URL = get_database_url()

# Initialize Heroku Postgres
init_db()

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
    """Run on message is sent."""
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


@client.event
async def on_raw_reaction_add(payload):
    """Run on reaction is made.

    When a member with `ROLE` reacts on `CHANNEL`, `ROLE` is given to the person who sent the message.
    """
    CHANNEL_ID, ROLE_ID, _ = get_ids(payload.guild_id)
    if None not in (CHANNEL_ID, ROLE_ID) and payload.channel_id == CHANNEL_ID:
        ROLE = get(payload.member.roles, id=ROLE_ID)
        if ROLE is not None:
            channel = client.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            member, = await message.guild.query_members(user_ids=[message.author.id])
            if ROLE not in member.roles:
                await member.add_roles(ROLE)

client.run(TOKEN)
