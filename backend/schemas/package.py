from typing import Any

from pydantic import BaseModel, Field


class PackageGenerateRequest(BaseModel):
    student_id: str = Field(default="stu_001")
    dialogue: str = Field(
        default="我是人工智能专业大二学生，逻辑回归里的 sigmoid 和损失函数看不懂，数学基础一般，但 Python 还可以。"
    )
    target_course: str = Field(default="机器学习基础")
    target_topic: str = Field(default="逻辑回归")


class PackageGenerateResponse(BaseModel):
    task_id: str
    status: str
    profile_agent_output: dict[str, Any]
    retrieval_agent_output: dict[str, Any]
    resource_agent_output: dict[str, Any]
    review_path_agent_output: dict[str, Any]
    resources: list[dict[str, Any]]
    learning_path: list[dict[str, Any]]
