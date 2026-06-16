from typing import Any

from backend.services.course_index_service import CourseIndexService


class RetrievalAgent:
    def __init__(self, course_index_service: CourseIndexService | None = None) -> None:
        self.course_index_service = course_index_service or CourseIndexService()

    def retrieve(self, profile: dict[str, Any], target_topic: str) -> dict[str, Any]:
        retrieval = self.course_index_service.retrieve(target_topic)
        matched_title = (
            retrieval.get("matched_chapter") or {}
        ).get("title", "未匹配章节")

        return {
            "agent": "RetrievalAgent",
            "input": {
                "profile_student_id": profile.get("student_id"),
                "target_topic": target_topic,
            },
            "found": retrieval["found"],
            "message": retrieval["message"],
            "matched_chapter": retrieval["matched_chapter"],
            "matched_knowledge_points": retrieval["matched_knowledge_points"],
            "source_refs": retrieval["source_refs"],
            "retrieved_context": retrieval["retrieved_context"],
            "agent_log": (
                f"RetrievalAgent 已真实读取 knowledge_base/index.json 和 Markdown 文件，"
                f"目标主题“{target_topic}”匹配结果：{matched_title}。"
            ),
        }
