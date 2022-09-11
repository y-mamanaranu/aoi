import psycopg2
import logging

_log = logging.getLogger(__name__)


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
                pending bigint DEFAULT 0,
                if_limit boolean DEFAULT false,
                if_adjust boolean DEFAULT false,
                if_move boolean DEFAULT false,
                if_create_voice boolean DEFAULT false,
                if_create_text boolean DEFAULT false,
                twitter_template text,
                twitter_access_token text,
                twitter_access_token_secret text,
                if_level boolean DEFAULT false,
                );""")

            if ('user_table',) not in res:
                cur.execute("""CREATE TABLE user_table (
                guild_id bigint NOT NULL,
                member_id bigint NOT NULL,
                last_join bigint DEFAULT 0,
                last_leave bigint DEFAULT 0,
                total bigint DEFAULT 0
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
               GUILD_ID: int):
    """Remove ids from database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""DELETE FROM reactedrole
            WHERE guild_id = %s;""",
                        (GUILD_ID, )
                        )
            conn.commit()


def get_twitter_status(DATABASE_URL: str,
                       GUILD_ID: int):
    """Get twitter authorize status."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT twitter_access_token, twitter_access_token_secret
            FROM reactedrole
            WHERE guild_id = %s;""",
                        (GUILD_ID,))
            res = cur.fetchone()

    if None in res:
        return "not Authorized"
    else:
        return "Authorized"


def get_pro_log_fre_sen_emo(DATABASE_URL: str,
                            GUILD_ID: int):
    """Get ids from database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT profile_id, log_id, freshman_id, senior_id, emoji_id
            FROM reactedrole
            WHERE guild_id = %s;""",
                        (GUILD_ID,))
            res = cur.fetchone()

    return res


def get_prefix(DATABASE_URL: str,
               GUILD_ID: int) -> str:
    """Get prefix from database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT prefix
            FROM reactedrole
            WHERE guild_id = %s;""",
                        (GUILD_ID,))
            res = cur.fetchone()

    return res[0]


def get_profile_id(DATABASE_URL: str,
                   GUILD_ID: int):
    """Get ID of #Profile from database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT profile_id
            FROM reactedrole
            WHERE guild_id = %s;""",
                        (GUILD_ID,))
            res = cur.fetchone()

    return res[0]


def get_log_id(DATABASE_URL: str,
               GUILD_ID: int):
    """Get ID of #Log from database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT log_id
            FROM reactedrole
            WHERE guild_id = %s;""",
                        (GUILD_ID,))
            res = cur.fetchone()

    return res[0]


def get_if_level(DATABASE_URL: str,
                 GUILD_ID: int) -> bool:
    """Get if_level from database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT if_level
            FROM reactedrole
            WHERE guild_id = %s;""",
                        (GUILD_ID,))
            res = cur.fetchone()

    return res[0]


def get_if_limit(DATABASE_URL: str,
                 GUILD_ID) -> bool:
    """Get if_limit from database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT if_limit
            FROM reactedrole
            WHERE guild_id = %s;""",
                        (GUILD_ID,))
            res = cur.fetchone()

    return res[0]


def get_if_adjust(DATABASE_URL: str,
                  GUILD_ID) -> bool:
    """Get if_adjust from database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT if_adjust
            FROM reactedrole
            WHERE guild_id = %s;""",
                        (GUILD_ID,))
            res = cur.fetchone()

    return res[0]


def get_if_move(DATABASE_URL: str,
                GUILD_ID) -> bool:
    """Get if_move from database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT if_move
            FROM reactedrole
            WHERE guild_id = %s;""",
                        (GUILD_ID,))
            res = cur.fetchone()

    return res[0]


def get_pending(DATABASE_URL: str,
                GUILD_ID) -> int:
    """Get pending from database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT pending
            FROM reactedrole
            WHERE guild_id = %s;""",
                        (GUILD_ID,))
            res = cur.fetchone()

    return res[0]


def get_icv_ict(DATABASE_URL: str,
                GUILD_ID: int):
    """Get ID of if_create_voice and if_create_text from database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT if_create_voice, if_create_text
            FROM reactedrole
            WHERE guild_id = %s;""",
                        (GUILD_ID,))
            res = cur.fetchone()

    return res


def get_tt_tat_tats(DATABASE_URL: str,
                    GUILD_ID: int):
    """Get twitter_template, twitter_access_token and twitter_access_token_secret from database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT twitter_template, twitter_access_token, twitter_access_token_secret
            FROM reactedrole
            WHERE guild_id = %s;""",
                        (GUILD_ID,))
            res = cur.fetchone()

    return res


def get_pre_pro_log_fre_sen_emo_ten_lim_adj_mov_icv_ict_tt(DATABASE_URL: str,

                                                           GUILD_ID: int):
    """Get status from database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT prefix,
            profile_id,
            log_id,
            freshman_id,
            senior_id,
            emoji_id,
            tenki_id,
            if_limit,
            if_adjust,
            if_move,
            if_create_voice,
            if_create_text,
            twitter_template
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


def update_profile_id(DATABASE_URL: str,
                      GUILD_ID, PROFILE_ID):
    """Update channle_id in database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE reactedrole
                SET profile_id = %s
                WHERE guild_id = %s;""",
                (PROFILE_ID, GUILD_ID))


def update_log_id(DATABASE_URL: str,
                  GUILD_ID, LOG_ID):
    """Update log_id in database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE reactedrole
                SET log_id = %s
                WHERE guild_id = %s;""",
                (LOG_ID, GUILD_ID))


def update_freshman_id(DATABASE_URL: str,
                       GUILD_ID, FRESHMAN_ID):
    """Update freshman_id in database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE reactedrole
                SET freshman_id = %s
                WHERE guild_id = %s;""",
                (FRESHMAN_ID, GUILD_ID))


def update_senior_id(DATABASE_URL: str,
                     GUILD_ID, SENIOR_ID):
    """Update senior_id in database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE reactedrole
                SET senior_id = %s
                WHERE guild_id = %s;""",
                (SENIOR_ID, GUILD_ID))


def update_emoji_id(DATABASE_URL: str,
                    GUILD_ID, EMOJI_ID):
    """Update emoji_id in database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE reactedrole
                SET emoji_id = %s
                WHERE guild_id = %s;""",
                (EMOJI_ID, GUILD_ID))


def update_if_move(DATABASE_URL: str,
                   GUILD_ID, IF_MOVE):
    """Update if_move in database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE reactedrole
                SET if_move = %s
                WHERE guild_id = %s;""",
                (IF_MOVE, GUILD_ID))


def update_if_limit(DATABASE_URL: str,
                    GUILD_ID, IF_LIMIT):
    """Update if_limit in database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE reactedrole
                SET if_limit = %s
                WHERE guild_id = %s;""",
                (IF_LIMIT, GUILD_ID))


def update_if_create_text(DATABASE_URL: str,
                          GUILD_ID, IF_CREATE_TEXT):
    """Update if_create_text in database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE reactedrole
                SET if_create_text = %s
                WHERE guild_id = %s;""",
                (IF_CREATE_TEXT, GUILD_ID))


def update_if_create_voice(DATABASE_URL: str,
                           GUILD_ID, IF_CREATE_VOICE):
    """Update if_create_voice in database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE reactedrole
                SET if_create_voice = %s
                WHERE guild_id = %s;""",
                (IF_CREATE_VOICE, GUILD_ID))


def update_if_adjust(DATABASE_URL: str,
                     GUILD_ID, IF_ADJUST):
    """Update if_adjust in database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE reactedrole
                SET if_adjust = %s
                WHERE guild_id = %s;""",
                (IF_ADJUST, GUILD_ID))


def update_prefix(DATABASE_URL: str,
                  GUILD_ID, PREFIX):
    """Update prefix in database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE reactedrole
                SET prefix = %s
                WHERE guild_id = %s;""",
                (PREFIX, GUILD_ID))


def update_tenki_id(DATABASE_URL: str,
                    GUILD_ID, TENKI_ID):
    """Update tenki_id in database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE reactedrole
                SET tenki_id = %s
                WHERE guild_id = %s;""",
                (TENKI_ID, GUILD_ID))


def update_pending(DATABASE_URL: str, GUILD_ID: str, PENDING: int):
    """Update pending in database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE reactedrole
                SET pending = %s
                WHERE guild_id = %s;""",
                (PENDING, GUILD_ID))


def update_twitter_template(DATABASE_URL: str,
                            GUILD_ID, TWITTER_TEMPLATE):
    """Update twitter_template in database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE reactedrole
                SET twitter_template = %s
                WHERE guild_id = %s;""",
                (TWITTER_TEMPLATE, GUILD_ID))


def update_tat_tats(DATABASE_URL: str,

                    GUILD_ID,
                    TWITTER_ACCESS_TOKEN,
                    TWITTER_ACCESS_TOKEN_SECRET):
    """Update twitter_access_token and twitter_access_token_secret in database."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE reactedrole
                SET twitter_access_token = %s,
                twitter_access_token_secret = %s
                WHERE guild_id = %s;""",
                (TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET, GUILD_ID))
