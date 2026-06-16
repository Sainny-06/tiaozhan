from typing import Any

from pydantic import BaseModel


class QuizAnswerItem(BaseModel):
    question_id: str
    student_answer: str


class QuizSubmitRequest(BaseModel):
    student_id: str
    topic: str
    answers: list[QuizAnswerItem]
    task_id: str | None = None


class QuizSubmitResponse(BaseModel):
    record_id: str
    score: float
    total_questions: int
    correct_count: int
    wrong_points: list[str]
    wrong_question_analysis: list[dict[str, Any]]
    profile_before: dict[str, Any]
    profile_after: dict[str, Any]
    profile_diff: list[dict[str, Any]]
    new_recommendations: list[dict[str, Any]]
    updated_learning_path: list[dict[str, Any]]
