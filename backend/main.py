from fastapi import FastAPI

from backend.config import APP_NAME
from backend.database.db import init_db
from backend.main_workflow import LearningPackageWorkflow
from backend.schemas.package import PackageGenerateRequest, PackageGenerateResponse

app = FastAPI(title=APP_NAME)


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
    return workflow.run(
        student_id=payload.student_id,
        dialogue=payload.dialogue,
        target_course=payload.target_course,
        target_topic=payload.target_topic,
    )
