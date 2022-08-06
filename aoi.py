import discord
from discord.utils import get
import os

# 自分のBotのアクセストークンに置き換えてください
TOKEN = os.environ["AOI_TOKEN"]
CHANNEL_ID = int(os.environ["AOI_CHANNEL_ID"])
ROLE_ID = int(os.environ["AOI_ROLE_ID"])

# 接続に必要なオブジェクトを生成
intents = discord.Intents.default()
intents.reactions = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    global ROLE
    # 起動したらターミナルにログイン通知が表示される
    print('Aoi is started')


@client.event
async def on_message(message):
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
    if message.content == ';text_channels':
        text = []
        for chann in message.guild.text_channels:
            text.append(f"{chann.name}: {chann.id}")
        await message.channel.send("\n".join(text))


@client.event
async def on_raw_reaction_add(payload):
    # CHANNELでROLEを持つメンバーがリアクションすると、メッセージを送った人にROLEを付与。
    if payload.channel_id == CHANNEL_ID:
        ROLE = get(payload.member.roles, id=ROLE_ID)
        if ROLE is not None:
            channel = client.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            member, = await message.guild.query_members(user_ids=[message.author.id])
            if ROLE not in member.roles:
                await member.add_roles(ROLE)

client.run(TOKEN)
