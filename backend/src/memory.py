import sqlite3
import json
from datetime import datetime

DB_PATH = "memory.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            name TEXT,
            language_preference TEXT,
            facts TEXT,
            last_interaction TEXT
        )
    """)

    conn.commit()
    conn.close()


def lookup_user(user_id: str):
    conn = sqlite3.connect(DB_PATH)

    cursor = conn.execute(
        "SELECT user_id, name, language_preference, facts, last_interaction "
        "FROM users WHERE user_id = ?",
        (user_id,),
    )

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    return {
        "user_id": row[0],
        "name": row[1],
        "language_preference": row[2],
        "facts": json.loads(row[3]) if row[3] else {},
        "last_interaction": row[4],
    }


def save_user(
    user_id: str,
    name: str,
    language_preference: str,
    facts: dict,
):
    conn = sqlite3.connect(DB_PATH)

    conn.execute(
        """
        INSERT OR REPLACE INTO users
        (user_id, name, language_preference, facts, last_interaction)
        VALUES (?, ?, ?, ?, ?)
    """,
        (
            user_id,
            name,
            language_preference,
            json.dumps(facts),
            datetime.now().isoformat(),
        ),
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized!")


def create_escalation(
    user_id: str,
    issue: str,
    summary: str,
    urgency: str,
    language: str,
    follow_up_method: str,
):
    """Create a human-support escalation request."""

    import sqlite3
    import uuid
    from datetime import datetime, timezone

    escalation_id = f"ESC-{uuid.uuid4().hex[:6].upper()}"

    created_at = datetime.now(timezone.utc).isoformat()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS escalations (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            issue TEXT NOT NULL,
            summary TEXT NOT NULL,
            urgency TEXT NOT NULL,
            language TEXT,
            follow_up_method TEXT,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """)

    cursor.execute(
        """
        INSERT INTO escalations (
            id,
            user_id,
            issue,
            summary,
            urgency,
            language,
            follow_up_method,
            status,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            escalation_id,
            user_id,
            issue,
            summary,
            urgency,
            language,
            follow_up_method,
            "open",
            created_at,
        ),
    )

    conn.commit()
    conn.close()

    return escalation_id
