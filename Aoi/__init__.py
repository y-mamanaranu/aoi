from distutils.sysconfig import PREFIX
import os
from unittest.mock import DEFAULT
import psycopg2

DEFAULT_CHANNEL_ID = None
DEFAULT_ROLE_ID = None
DEFAULT_ADMIN_ROLE_ID = None
DEFAULT_PREFIX = ";"


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
                channel_id bigint,
                role_id bigint,
                admin_role_id bigint,
                prefix text
                );""")


def insert_ids(DATABASE_URL: str,
               GUILD_ID: int,
               CHANNEL_ID: int,
               ROLE_ID: int,
               ADMIN_ROLE_ID: int,
               PREFIX: str):
    """Insert new ids into database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""INSERT INTO reactedrole (
                guild_id,
                channel_id,
                role_id,
                admin_role_id,
                prefix
                ) VALUES(%s, %s, %s, %s, %s);""",
                        (GUILD_ID, CHANNEL_ID, ROLE_ID, ADMIN_ROLE_ID, PREFIX)
                        )
            conn.commit()


def get_ids(DATABASE_URL, GUILD_ID):
    """Get ids from database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT channel_id, role_id, admin_role_id
            FROM reactedrole
            WHERE guild_id = %s;""",
                        (GUILD_ID,))
            res = cur.fetchone()

    if res is None:
        insert_ids(
            DATABASE_URL,
            GUILD_ID,
            DEFAULT_CHANNEL_ID,
            DEFAULT_ROLE_ID,
            DEFAULT_ADMIN_ROLE_ID,
            DEFAULT_PREFIX)
        return DEFAULT_CHANNEL_ID, DEFAULT_ROLE_ID, DEFAULT_ADMIN_ROLE_ID
    else:
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

    if res is None:
        insert_ids(
            DATABASE_URL,
            GUILD_ID,
            DEFAULT_CHANNEL_ID,
            DEFAULT_ROLE_ID,
            DEFAULT_ADMIN_ROLE_ID,
            DEFAULT_PREFIX)
        return DEFAULT_PREFIX
    else:
        return res[0]


def get_admin_role_id(DATABASE_URL, GUILD_ID):
    """Get ID of admin role from database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT admin_role_id
            FROM reactedrole
            WHERE guild_id = %s;""",
                        (GUILD_ID,))
            res = cur.fetchone()

    if res is None:
        insert_ids(
            DATABASE_URL,
            GUILD_ID,
            DEFAULT_CHANNEL_ID,
            DEFAULT_ROLE_ID,
            DEFAULT_ADMIN_ROLE_ID,
            DEFAULT_PREFIX)
        return DEFAULT_ADMIN_ROLE_ID
    else:
        return res[0]


def get_status(DATABASE_URL, GUILD_ID):
    """Get status from database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT channel_id, role_id, admin_role_id, prefix
            FROM reactedrole
            WHERE guild_id = %s;""",
                        (GUILD_ID,))
            res = cur.fetchone()

    if res is None:
        insert_ids(
            DATABASE_URL,
            GUILD_ID,
            DEFAULT_CHANNEL_ID,
            DEFAULT_ROLE_ID,
            DEFAULT_ADMIN_ROLE_ID,
            DEFAULT_PREFIX)
        return DEFAULT_CHANNEL_ID, DEFAULT_ROLE_ID, DEFAULT_ADMIN_ROLE_ID, DEFAULT_PREFIX
    else:
        return res


def update_channel_id(DATABASE_URL, GUILD_ID, CHANNEL_ID):
    """Update channle_id in database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE reactedrole
                SET channel_id = %s
                WHERE guild_id = %s;""",
                (CHANNEL_ID, GUILD_ID))


def update_role_id(DATABASE_URL, GUILD_ID, ROLE_ID):
    """Update role_id in database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE reactedrole
                SET role_id = %s
                WHERE guild_id = %s;""",
                (ROLE_ID, GUILD_ID))


def update_admin_role_id(DATABASE_URL, GUILD_ID, ADMIN_ROLE_ID):
    """Update admin_role_id in database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE reactedrole
                SET admin_role_id = %s
                WHERE guild_id = %s;""",
                (ADMIN_ROLE_ID, GUILD_ID))


def update_prefix(DATABASE_URL, GUILD_ID, PREFIX):
    """Update prefix in database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE reactedrole
                SET prefix = %s
                WHERE guild_id = %s;""",
                (PREFIX, GUILD_ID))
