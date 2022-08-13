from discord.utils import get
import os
import psycopg2
import re

DEFAULT_PROFILE_ID = None
DEFAULT_FRESHMAN_ID = None
DEFAULT_SENIOR_ID = None
DEFAULT_ADMIN_ID = None
DEFAULT_PREFIX = ";"
DEFAULT_LOG_ID = None


def convert_mention_to_user(mention: str):
    """Convert mention to user to user_id."""
    res = re.match(r"^<@(\d+)>$", mention)
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


async def check_privilage(DATABASE_URL, GUILD_ID, message):
    """"Check user hold Admin role."""
    ADMIN_ID = get_admin_id(DATABASE_URL, GUILD_ID)
    if ADMIN_ID is not None:
        role = get(message.guild.roles, id=ADMIN_ID)
        if role is not None:
            role = get(message.author.roles, id=ADMIN_ID)
            if role is None:
                await message.channel.send("""You don't have privilege to excute this command.""")
                return False
            else:
                return True
        else:
            await message.channel.send(f"""ID of admin role of {ADMIN_ID} is set, """
                                       """but corresponding role is not found. """
                                       """Config command is allowed to all members.""")
            return True
    else:
        await message.channel.send("""ID of admin role is not set. """
                                   """Config command is allowed to all members.""")
        return True


def get_token():
    """Get token of Discord bot."""
    return os.environ["TOKEN"]


def get_database_url():
    """Get database URL of Heroku Postgres."""
    return os.environ["DATABASE_URL"]


def init_db(DATABASE_URL):
    """Initialize database."""
    # table一覧を取得
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public';""")
            res = cur.fetchall()

            # reactedroleが無い時は作成
            if ('reactedrole',) not in res:
                cur.execute("""CREATE TABLE reactedrole (
                guild_id bigint PRIMARY KEY,
                prefix text,
                profile_id bigint,
                log_id bigint,
                freshman_id bigint,
                senior_id bigint,
                admin_id bigint,
                );""")


def insert_ids(DATABASE_URL: str,
               GUILD_ID: int):
    """Insert new ids into database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""INSERT INTO reactedrole (
                guild_id,
                prefix,
                profile_id,
                log_id,
                freshman_id,
                senior_id,
                admin_id
                ) VALUES(%s, %s, %s, %s, %s, %s);""",
                        (GUILD_ID,
                         DEFAULT_PREFIX,
                         DEFAULT_PROFILE_ID,
                         DEFAULT_LOG_ID,
                         DEFAULT_FRESHMAN_ID,
                         DEFAULT_SENIOR_ID,
                         DEFAULT_ADMIN_ID)
                        )
            conn.commit()


def remove_ids(DATABASE_URL: str,
               GUILD_ID: str):
    """Remove ids from database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""DELETE FROM reactedrole
            WHERE guild_id = %s;""",
                        (GUILD_ID, )
                        )
            conn.commit()


def get_pro_log_fre_sen(DATABASE_URL, GUILD_ID):
    """Get ids from database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT profile_id, log_id, freshman_id, senior_id
            FROM reactedrole
            WHERE guild_id = %s;""",
                        (GUILD_ID,))
            res = cur.fetchone()

    return res


def get_prefix(DATABASE_URL, GUILD_ID):
    """Get prefix from database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT prefix
            FROM reactedrole
            WHERE guild_id = %s;""",
                        (GUILD_ID,))
            res = cur.fetchone()

    return res[0]


def get_profile_id(DATABASE_URL, GUILD_ID):
    """Get ID of admin role from database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT profile_id
            FROM reactedrole
            WHERE guild_id = %s;""",
                        (GUILD_ID,))
            res = cur.fetchone()

    return res[0]


def get_log_id(DATABASE_URL, GUILD_ID):
    """Get ID of admin role from database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT log_id
            FROM reactedrole
            WHERE guild_id = %s;""",
                        (GUILD_ID,))
            res = cur.fetchone()

    return res[0]


def get_admin_id(DATABASE_URL, GUILD_ID):
    """Get ID of admin role from database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT admin_id
            FROM reactedrole
            WHERE guild_id = %s;""",
                        (GUILD_ID,))
            res = cur.fetchone()

    return res[0]


def get_pre_pro_log_fre_sen_adm(DATABASE_URL, GUILD_ID):
    """Get status from database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT prefix, profile_id, log_id, freshman_id, senior_id, admin_id
            FROM reactedrole
            WHERE guild_id = %s;""",
                        (GUILD_ID,))
            res = cur.fetchone()

    return res


def update_profile_id(DATABASE_URL, GUILD_ID, PROFILE_ID):
    """Update channle_id in database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE reactedrole
                SET profile_id = %s
                WHERE guild_id = %s;""",
                (PROFILE_ID, GUILD_ID))


def update_log_id(DATABASE_URL, GUILD_ID, LOG_ID):
    """Update log_id in database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE reactedrole
                SET log_id = %s
                WHERE guild_id = %s;""",
                (LOG_ID, GUILD_ID))


def update_freshman_id(DATABASE_URL, GUILD_ID, FRESHMAN_ID):
    """Update freshman_id in database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE reactedrole
                SET freshman_id = %s
                WHERE guild_id = %s;""",
                (FRESHMAN_ID, GUILD_ID))


def update_senior_id(DATABASE_URL, GUILD_ID, SENIOR_ID):
    """Update senior_id in database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE reactedrole
                SET senior_id = %s
                WHERE guild_id = %s;""",
                (SENIOR_ID, GUILD_ID))


def update_admin_id(DATABASE_URL, GUILD_ID, ADMIN_ID):
    """Update admin_id in database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE reactedrole
                SET admin_id = %s
                WHERE guild_id = %s;""",
                (ADMIN_ID, GUILD_ID))


def update_prefix(DATABASE_URL, GUILD_ID, PREFIX):
    """Update prefix in database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE reactedrole
                SET prefix = %s
                WHERE guild_id = %s;""",
                (PREFIX, GUILD_ID))
