import os
import psycopg2


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
                admin_role_id bigint
                );""")


def insert_ids(DATABASE_URL, GUILD_ID, CHANNEL_ID, ROLE_ID, ADMIN_ROLE_ID):
    """Insert new ids into database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""INSERT INTO reactedrole (
                guild_id,
                channel_id,
                role_id,
                admin_role_id
                ) VALUES(%s, %s, %s, %s);""",
                        (GUILD_ID, CHANNEL_ID, ROLE_ID, ADMIN_ROLE_ID)
                        )
            conn.commit()


def get_ids(DATABASE_URL, GUILD_ID):
    """Get ids from database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT *
            FROM reactedrole
            WHERE guild_id = %s;""",
                        (GUILD_ID,))
            res = cur.fetchone()

    if res is None:
        CHANNEL_ID, ROLE_ID, ADMIN_ROLE_ID = None, None, None
        insert_ids(GUILD_ID, CHANNEL_ID, ROLE_ID, ADMIN_ROLE_ID)
    else:
        _, CHANNEL_ID, ROLE_ID, ADMIN_ROLE_ID = res

    return CHANNEL_ID, ROLE_ID, ADMIN_ROLE_ID


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
