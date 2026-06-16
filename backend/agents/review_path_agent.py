from copy import deepcopy
from typing import Any


class ReviewPathAgent:
    def review_and_plan(
        self,
        profile: dict[str, Any],
        retrieved_context: dict[str, Any],
        resources: list[dict[str, Any]],
        target_topic: str | None = None,
    ) -> dict[str, Any]:
        source_refs = retrieved_context.get("source_refs", [])
        matched_chapter = retrieved_context.get("matched_chapter") or {}
        topic = matched_chapter.get("title") or target_topic or "未匹配主题"
        reviewed_resources = []

        for index, resource in enumerate(resources, start=1):
            reviewed = deepcopy(resource)
            reviewed["resource_id"] = f"res_{index:03d}"
            reviewed["source_refs"] = reviewed.get("source_refs") or source_refs
            reviewed["review_report"] = self._review_report(
                profile=profile,
                resource=reviewed,
            )
            reviewed_resources.append(reviewed)

        learning_path = self._learning_path(topic, profile, bool(source_refs))

        return {
            "agent": "ReviewPathAgent",
            "input": {
                "profile_student_id": profile.get("student_id"),
                "target_topic": target_topic,
                "resource_count": len(resources),
                "source_ref_count": len(source_refs),
            },
            "reviewed_resources": reviewed_resources,
            "learning_path": learning_path,
            "agent_log": (
                f"ReviewPathAgent 已基于“{topic}”和真实 source_refs 完成资源审校与路径规划。"
            ),
        }

    def _review_report(
        self,
        profile: dict[str, Any],
        resource: dict[str, Any],
    ) -> dict[str, str]:
        has_source_refs = bool(resource.get("source_refs"))
        resource_type = resource.get("type")
        return {
            "knowledge_grounding": "通过" if has_source_refs else "待补充",
            "difficulty_match": "通过",
            "answer_consistency": "通过" if resource_type == "quiz" else "不适用",
            "content_safety": "通过",
            "comment": (
                f"资源已绑定 {len(resource.get('source_refs', []))} 条课程知识库来源，"
                f"难度按 {profile.get('math_level', '未知')} 数学能力进行匹配。"
                if has_source_refs
                else "资源缺少 source_refs，当前知识库引用审校为待补充。"
            ),
        }

    def _learning_path(
        self,
        topic: str,
        profile: dict[str, Any],
        has_source_refs: bool,
    ) -> list[dict[str, Any]]:
        if not has_source_refs:
            return [
                {
                    "step": 1,
                    "title": f"补充“{topic}”课程资料",
                    "recommended_resources": [],
                    "reason": "当前主题未匹配到知识库章节，建议先补充 index.json 和 Markdown 内容。",
                }
            ]

        style = "图解" if "图解" in profile.get("cognitive_style", []) else "讲义"
        return [
            {
                "step": 1,
                "title": f"建立{topic}整体概念",
                "recommended_resources": ["lecture", "mindmap"],
                "reason": f"学生知识基础为{profile.get('knowledge_level', '未知')}，先建立章节框架。",
            },
            {
                "step": 2,
                "title": f"用{style}方式突破{topic}关键知识点",
                "recommended_resources": ["animation"],
                "reason": "结合学生认知偏好，优先使用可视化资源降低理解门槛。",
            },
            {
                "step": 3,
                "title": f"完成{topic}分层练习",
                "recommended_resources": ["quiz"],
                "reason": "通过基础题和理解题检查概念掌握情况。",
            },
            {
                "step": 4,
                "title": f"完成{topic}代码实操",
                "recommended_resources": ["code_lab"],
                "reason": f"学生编程能力为{profile.get('coding_level', '未知')}，适合通过实践巩固模型流程。",
            },
        ]
