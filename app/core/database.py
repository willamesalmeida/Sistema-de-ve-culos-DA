"""
database.py
Handles database connection, schema initialization and migrations.
"""

import os
import sqlite3
from sqlite3 import Connection

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DB_NAME = "fleet.db"
SCHEMA_VERSION = 1


# ---------------------------------------------------------------------------
# Connection
# ---------------------------------------------------------------------------

def get_db_path() -> str:
    """Returns the absolute path to the SQLite database file."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "..", "data", DB_NAME)


def get_connection() -> Connection:
    """
    Opens and returns a connection to the SQLite database.
    Rows are accessible by column name (e.g. row['name']).
    """
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ---------------------------------------------------------------------------
# Migrations
# ---------------------------------------------------------------------------

def _get_schema_version(conn: Connection) -> int:
    """Returns the current schema version stored in the database."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS schema_version (
            version INTEGER NOT NULL
        )
    """)
    row = conn.execute("SELECT version FROM schema_version").fetchone()
    return row["version"] if row else 0


def _set_schema_version(conn: Connection, version: int) -> None:
    """Updates the schema version in the database."""
    conn.execute("DELETE FROM schema_version")
    conn.execute("INSERT INTO schema_version (version) VALUES (?)", (version,))


def migrate(conn: Connection) -> None:
    """
    Runs all pending migrations in order.
    Safe to call on every application startup.

    To add a new migration in the future:
        1. Increment SCHEMA_VERSION constant
        2. Add a new block: if current_version < N: ...
    """
    current_version = _get_schema_version(conn)

    if current_version < 1:
        _migrate_v1(conn)

    _set_schema_version(conn, SCHEMA_VERSION)


# ---------------------------------------------------------------------------
# Schema versions
# ---------------------------------------------------------------------------

def _migrate_v1(conn: Connection) -> None:
    """V1 — initial schema: drivers and vehicles tables."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS drivers (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            cpf         TEXT,
            phone       TEXT,
            department  TEXT,
            photo_path  TEXT,
            created_at  TEXT    DEFAULT (datetime('now', 'localtime')),
            updated_at  TEXT    DEFAULT (datetime('now', 'localtime'))
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            plate       TEXT    NOT NULL UNIQUE,
            model       TEXT,
            driver_id   INTEGER,
            created_at  TEXT    DEFAULT (datetime('now', 'localtime')),
            updated_at  TEXT    DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (driver_id) REFERENCES drivers (id)
                ON UPDATE CASCADE
                ON DELETE SET NULL
        )
    """)


# ---------------------------------------------------------------------------
# Initialization
# ---------------------------------------------------------------------------

def initialize_database() -> None:
    """
    Initializes the database and runs pending migrations.
    Must be called once on application startup.
    """
    with get_connection() as conn:
        migrate(conn)


# ---------------------------------------------------------------------------
# Entry point (for isolated testing only)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    initialize_database()
    print(f"Database initialized at: {get_db_path()}")
    print(f"Schema version: {SCHEMA_VERSION}")