import json
import sqlite3
from datetime import datetime
from typing import Any

from backend.config import DATABASE_PATH
from backend.database.db import init_db


class StorageService:
    def __init__(self) -> None:
        init_db()

    def save_package(self, package: dict[str, Any]) -> None:
        profile = package.get("profile_agent_output", {}).get("profile", {})
        student_id = profile.get("student_id")
        target_topic = package.get("target_topic")
        if not student_id or not target_topic:
            return

        with self._connect() as connection:
            connection.execute(
                """
                INSERT OR REPLACE INTO learning_packages
                (task_id, student_id, target_topic, package_json, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    package["task_id"],
                    student_id,
                    target_topic,
                    self._dumps(package),
                    self._now(),
                ),
            )

    def get_package_by_task_id(self, task_id: str) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT package_json FROM learning_packages WHERE task_id = ?",
                (task_id,),
            ).fetchone()
        return self._loads(row["package_json"]) if row else None

    def get_latest_package(self, student_id: str, topic: str) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT package_json FROM learning_packages
                WHERE student_id = ? AND target_topic = ?
                ORDER BY created_at DESC
                LIMIT 1
                """,
                (student_id, topic),
            ).fetchone()
        return self._loads(row["package_json"]) if row else None

    def save_profile(self, student_id: str, profile: dict[str, Any]) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT OR REPLACE INTO student_profiles
                (student_id, profile_json, updated_at)
                VALUES (?, ?, ?)
                """,
                (student_id, self._dumps(profile), self._now()),
            )

    def get_profile(self, student_id: str) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT profile_json FROM student_profiles WHERE student_id = ?",
                (student_id,),
            ).fetchone()
        return self._loads(row["profile_json"]) if row else None

    def save_quiz_record(self, record: dict[str, Any]) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT OR REPLACE INTO quiz_records
                (
                    record_id,
                    student_id,
                    topic,
                    score,
                    wrong_points_json,
                    profile_before_json,
                    profile_after_json,
                    profile_diff_json,
                    new_recommendations_json,
                    updated_learning_path_json,
                    record_json,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record["record_id"],
                    record["student_id"],
                    record["topic"],
                    record["score"],
                    self._dumps(record["wrong_points"]),
                    self._dumps(record["profile_before"]),
                    self._dumps(record["profile_after"]),
                    self._dumps(record["profile_diff"]),
                    self._dumps(record["new_recommendations"]),
                    self._dumps(record["updated_learning_path"]),
                    self._dumps(record),
                    self._now(),
                ),
            )

    def get_quiz_record(self, record_id: str) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT record_json FROM quiz_records WHERE record_id = ?",
                (record_id,),
            ).fetchone()
        return self._loads(row["record_json"]) if row else None

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(DATABASE_PATH)
        connection.row_factory = sqlite3.Row
        return connection

    def _dumps(self, value: Any) -> str:
        return json.dumps(value, ensure_ascii=False)

    def _loads(self, value: str) -> Any:
        return json.loads(value)

    def _now(self) -> str:
        return datetime.now().isoformat(timespec="seconds")
