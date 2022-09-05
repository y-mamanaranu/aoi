import psycopg2


def init_db(DATABASE_URL):
    """Initialize database."""
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
                prefix text DEFAULT ';',
                profile_id bigint,
                log_id bigint,
                freshman_id bigint,
                senior_id bigint,
                emoji_id text,
                tenki_id bigint,
                if_limit boolean DEFAULT true,
                if_adjust boolean DEFAULT true,
                );""")


def insert_ids(DATABASE_URL: str,
               GUILD_ID: int):
    """Insert new ids into database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""INSERT INTO reactedrole (
                guild_id,
                ) VALUES(%s,);""",
                        (GUILD_ID,)
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


def get_pro_log_fre_sen_emo(DATABASE_URL, GUILD_ID):
    """Get ids from database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT profile_id, log_id, freshman_id, senior_id, emoji_id
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
    """Get ID of #Profile from database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT profile_id
            FROM reactedrole
            WHERE guild_id = %s;""",
                        (GUILD_ID,))
            res = cur.fetchone()

    return res[0]


def get_log_id(DATABASE_URL, GUILD_ID):
    """Get ID of #Log from database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT log_id
            FROM reactedrole
            WHERE guild_id = %s;""",
                        (GUILD_ID,))
            res = cur.fetchone()

    return res[0]


def get_if_limit(DATABASE_URL, GUILD_ID):
    """Get if_limit from database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT if_limit
            FROM reactedrole
            WHERE guild_id = %s;""",
                        (GUILD_ID,))
            res = cur.fetchone()

    return res[0]


def get_if_adjust(DATABASE_URL, GUILD_ID):
    """Get if_adjust from database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT if_adjust
            FROM reactedrole
            WHERE guild_id = %s;""",
                        (GUILD_ID,))
            res = cur.fetchone()

    return res[0]


def get_pre_pro_log_fre_sen_emo_ten_lim_adj(DATABASE_URL, GUILD_ID):
    """Get status from database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT prefix, profile_id, log_id, freshman_id, senior_id, emoji_id, tenki_id, if_limit, if_adjust
            FROM reactedrole
            WHERE guild_id = %s;""",
                        (GUILD_ID,))
            res = cur.fetchone()

    return res


def get_all_tenki_id(DATABASE_URL):
    """Get ID of #Tenki from database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT tenki_id
            FROM reactedrole
            WHERE tenki_id IS NOT NULL;""")
            res = cur.fetchall()

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


def update_emoji_id(DATABASE_URL, GUILD_ID, EMOJI_ID):
    """Update emoji_id in database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE reactedrole
                SET emoji_id = %s
                WHERE guild_id = %s;""",
                (EMOJI_ID, GUILD_ID))


def update_if_limit(DATABASE_URL, GUILD_ID, IF_LIMIT):
    """Update if_limit in database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE reactedrole
                SET if_limit = %s
                WHERE guild_id = %s;""",
                (IF_LIMIT, GUILD_ID))


def update_if_adjust(DATABASE_URL, GUILD_ID, IF_ADJUST):
    """Update if_adjust in database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE reactedrole
                SET if_adjust = %s
                WHERE guild_id = %s;""",
                (IF_ADJUST, GUILD_ID))


def update_prefix(DATABASE_URL, GUILD_ID, PREFIX):
    """Update prefix in database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE reactedrole
                SET prefix = %s
                WHERE guild_id = %s;""",
                (PREFIX, GUILD_ID))


def update_tenki_id(DATABASE_URL, GUILD_ID, TENKI_ID):
    """Update tenki_id in database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE reactedrole
                SET tenki_id = %s
                WHERE guild_id = %s;""",
                (TENKI_ID, GUILD_ID))
