from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.agents.profile_agent import ProfileAgent
from backend.config import APP_NAME
from backend.database.db import init_db
from backend.main_workflow import LearningPackageWorkflow
from backend.schemas.package import PackageGenerateRequest, PackageGenerateResponse
from backend.schemas.quiz import QuizSubmitRequest, QuizSubmitResponse
from backend.services.course_index_service import CourseIndexService
from backend.services.quiz_service import QuizService
from backend.services.recommendation_service import RecommendationService
from backend.services.storage_service import StorageService

app = FastAPI(title=APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": APP_NAME,
    }


@app.post("/api/package/generate", response_model=PackageGenerateResponse)
def generate_package(payload: PackageGenerateRequest) -> dict:
    workflow = LearningPackageWorkflow()
    result = workflow.run(
        student_id=payload.student_id,
        dialogue=payload.dialogue,
        target_course=payload.target_course,
        target_topic=payload.target_topic,
    )
    storage = StorageService()
    storage.save_package(result)
    storage.save_profile(
        payload.student_id,
        result["profile_agent_output"]["profile"],
    )
    return result


@app.get("/api/knowledge/index")
def get_knowledge_index() -> dict:
    return CourseIndexService().get_index_summary()


@app.get("/api/knowledge/chapter/{chapter_id}")
def get_knowledge_chapter(chapter_id: str) -> dict:
    return CourseIndexService().get_chapter(chapter_id)


@app.post("/api/quiz/submit", response_model=QuizSubmitResponse)
def submit_quiz(payload: QuizSubmitRequest) -> dict:
    storage = StorageService()
    package = None
    if payload.task_id:
        package = storage.get_package_by_task_id(payload.task_id)
    else:
        package = storage.get_latest_package(payload.student_id, payload.topic)

    if not package:
        raise HTTPException(
            status_code=404,
            detail="未找到对应资源包，请先调用 /api/package/generate 生成资源包。",
        )

    quiz_result = QuizService().grade(
        package=package,
        answers=[item.model_dump() for item in payload.answers],
    )
    if not quiz_result.get("ok"):
        raise HTTPException(status_code=404, detail=quiz_result["error"])

    profile_before = (
        storage.get_profile(payload.student_id)
        or package.get("profile_agent_output", {}).get("profile")
        or {}
    )
    profile_update = ProfileAgent().update_profile_after_quiz(
        old_profile=profile_before,
        quiz_result=quiz_result,
    )
    profile_after = profile_update["profile_after"]
    profile_diff = profile_update["profile_diff"]
    recommendation_result = RecommendationService().generate(
        wrong_points=quiz_result["wrong_points"],
        topic=payload.topic,
    )

    record = {
        "record_id": f"quiz_{uuid4().hex[:12]}",
        "student_id": payload.student_id,
        "topic": payload.topic,
        "score": quiz_result["score"],
        "total_questions": quiz_result["total_questions"],
        "correct_count": quiz_result["correct_count"],
        "wrong_points": quiz_result["wrong_points"],
        "wrong_question_analysis": quiz_result["wrong_question_analysis"],
        "profile_before": profile_before,
        "profile_after": profile_after,
        "profile_diff": profile_diff,
        "new_recommendations": recommendation_result["new_recommendations"],
        "updated_learning_path": recommendation_result["updated_learning_path"],
    }

    storage.save_profile(payload.student_id, profile_after)
    storage.save_quiz_record(record)
    return record


@app.get("/api/profile/{student_id}")
def get_profile(student_id: str) -> dict:
    profile = StorageService().get_profile(student_id)
    if not profile:
        raise HTTPException(status_code=404, detail="未找到学生画像。")
    return profile


@app.get("/api/quiz/{record_id}")
def get_quiz_record(record_id: str) -> dict:
    record = StorageService().get_quiz_record(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="未找到测验记录。")
    return record
