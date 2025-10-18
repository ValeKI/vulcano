from config import CURRENT_CONFIG
from psycopg2.extras import RealDictCursor
import psycopg2

conn = psycopg2.connect(
    host=CURRENT_CONFIG.DB_HOST,
    port=CURRENT_CONFIG.DB_PORT,
    database=CURRENT_CONFIG.DB_NAME,
    user=CURRENT_CONFIG.DB_USER,
    password=CURRENT_CONFIG.DB_PASSWORD
)


def get_cursor():
    return conn.cursor(cursor_factory=RealDictCursor)