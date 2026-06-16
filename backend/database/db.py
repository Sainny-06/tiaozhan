import sqlite3

from backend.config import DATABASE_PATH


def init_db() -> None:
    """Initialize the minimal SQLite tables required by the MVP backend."""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS student_profiles (
                student_id TEXT PRIMARY KEY,
                profile_json TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS learning_packages (
                task_id TEXT PRIMARY KEY,
                student_id TEXT NOT NULL,
                target_topic TEXT NOT NULL,
                package_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS quiz_records (
                record_id TEXT PRIMARY KEY,
                student_id TEXT NOT NULL,
                topic TEXT NOT NULL,
                score REAL NOT NULL,
                wrong_points_json TEXT NOT NULL,
                profile_before_json TEXT NOT NULL,
                profile_after_json TEXT NOT NULL,
                profile_diff_json TEXT NOT NULL,
                new_recommendations_json TEXT NOT NULL,
                updated_learning_path_json TEXT NOT NULL,
                record_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
