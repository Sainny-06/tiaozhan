import sqlite3

from backend.config import DATABASE_PATH


def init_db() -> None:
    """Create the SQLite file for phase 1 without adding business tables yet."""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DATABASE_PATH):
        pass
