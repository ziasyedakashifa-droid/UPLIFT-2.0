import sqlite3
import json
from datetime import datetime, timezone

DB = "uplift_demo.db"


def conn():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c


def now():
    return datetime.now(timezone.utc).isoformat()


def init_db():
    with conn() as c:

        # Student accounts
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE COLLATE NOCASE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        # Mood records
        c.execute("""
            CREATE TABLE IF NOT EXISTS moods (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                score INTEGER,
                created_at TEXT
            )
        """)

        # Journal records
        c.execute("""
            CREATE TABLE IF NOT EXISTS journals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                entry TEXT,
                emotions TEXT,
                stressors TEXT,
                created_at TEXT
            )
        """)

        # HumanConnect requests
        c.execute("""
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                concern TEXT,
                contact TEXT,
                status TEXT,
                created_at TEXT
            )
        """)

        # Safely upgrade existing databases.
        # Existing records are preserved.

        for table in ["moods", "journals", "requests"]:
            columns = [
                row["name"]
                for row in c.execute(
                    f"PRAGMA table_info({table})"
                ).fetchall()
            ]

            if "user_id" not in columns:
                c.execute(
                    f"ALTER TABLE {table} ADD COLUMN user_id INTEGER"
                )


def create_user(name, email, password_hash):
    with conn() as c:
        c.execute("""
            INSERT INTO users (name, email, password_hash, created_at)
            VALUES (?, ?, ?, ?)
        """, (name, email, password_hash, now()))


def get_user_by_email(email):
    with conn() as c:
        user = c.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

    return dict(user) if user else None


def get_user_by_id(user_id):
    with conn() as c:
        user = c.execute(
            "SELECT id, name, email FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()

    return dict(user) if user else None


def save_mood(user_id, score):
    with conn() as c:
        c.execute("""
            INSERT INTO moods (user_id, score, created_at)
            VALUES (?, ?, ?)
        """, (user_id, score, now()))


def get_moods(user_id):
    with conn() as c:
        rows = c.execute("""
            SELECT score, created_at
            FROM moods
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT 14
        """, (user_id,)).fetchall()

    return [dict(x) for x in reversed(rows)]


def save_journal(user_id, entry, emotions, stressors):
    with conn() as c:
        c.execute("""
            INSERT INTO journals
            (user_id, entry, emotions, stressors, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            user_id,
            entry,
            json.dumps(emotions),
            json.dumps(stressors),
            now()
        ))


def create_support_request(user_id, concern, contact):
    with conn() as c:
        c.execute("""
            INSERT INTO requests
            (user_id, concern, contact, status, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            user_id,
            concern,
            contact,
            "Pending",
            now()
        ))


def get_support_requests():
    with conn() as c:
        rows = c.execute("""
            SELECT requests.*, users.name, users.email
            FROM requests
            LEFT JOIN users ON requests.user_id = users.id
            ORDER BY requests.id DESC
        """).fetchall()

    return [dict(x) for x in rows]