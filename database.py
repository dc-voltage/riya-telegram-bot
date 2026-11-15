import sqlite3
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), "bot_database.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                first_seen TEXT,
                last_seen TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT,
                timestamp TEXT
            )
        """)
        conn.commit()
    logger.info("Database initialized successfully.")

def record_user(user_id: int, username: str, first_name: str):
    now = datetime.now().isoformat()
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (user_id, username, first_name, first_seen, last_seen)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    username=excluded.username,
                    first_name=excluded.first_name,
                    last_seen=excluded.last_seen
            """, (user_id, username or "", first_name or "Friend", now, now))
            conn.commit()
    except Exception as e:
        logger.warning(f"Error recording user {user_id}: {e}")

def record_event(event_type: str):
    now = datetime.now().isoformat()
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO stats (event_type, timestamp) VALUES (?, ?)", (event_type, now))
            conn.commit()
    except Exception as e:
        logger.warning(f"Error recording event {event_type}: {e}")

def get_all_users():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, first_name FROM users")
        return cursor.fetchall()

def get_setting(key: str, default=None):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)")
            cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
            row = cursor.fetchone()
            return row[0] if row else default
    except Exception as e:
        logger.warning(f"Error reading setting {key}: {e}")
        return default

def set_setting(key: str, value: str):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)")
            cursor.execute("""
                INSERT INTO settings (key, value) VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET value=excluded.value
            """, (key, str(value)))
            conn.commit()
    except Exception as e:
        logger.warning(f"Error saving setting {key}: {e}")

def get_db_stats():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]

        cursor.execute("SELECT event_type, COUNT(*) FROM stats GROUP BY event_type")
        event_counts = dict(cursor.fetchall())

        return {
            "total_users": total_users,
            "text_queries": event_counts.get("text_query", 0),
            "voice_queries": event_counts.get("voice_query", 0),
            "image_queries": event_counts.get("image_query", 0),
            "total_events": sum(event_counts.values())
        }
