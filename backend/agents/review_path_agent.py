from copy import deepcopy
from typing import Any


class ReviewPathAgent:
    def review_and_plan(
        self,
        profile: dict[str, Any],
        retrieved_context: dict[str, Any],
        resources: list[dict[str, Any]],
    ) -> dict[str, Any]:
        source_refs = retrieved_context.get("source_refs", [])
        reviewed_resources = []

        for index, resource in enumerate(resources, start=1):
            reviewed = deepcopy(resource)
            reviewed["resource_id"] = f"res_{index:03d}"
            reviewed.setdefault("source_refs", source_refs)
            reviewed.setdefault("review_report", self._review_report(profile))
            reviewed_resources.append(reviewed)

        learning_path = [
            {
                "step": 1,
                "title": "理解逻辑回归解决什么问题",
                "recommended_resources": ["lecture", "mindmap"],
                "reason": "学生数学基础较弱，先建立整体概念和知识结构。",
            },
            {
                "step": 2,
                "title": "通过图解理解 Sigmoid 函数",
                "recommended_resources": ["animation"],
                "reason": "学生偏好图解，且 Sigmoid 函数是当前薄弱点。",
            },
            {
                "step": 3,
                "title": "完成分层练习题",
                "recommended_resources": ["quiz"],
                "reason": "通过基础题和理解题检查关键概念。",
            },
            {
                "step": 4,
                "title": "完成 Python 代码实操",
                "recommended_resources": ["code_lab"],
                "reason": "学生编程能力较强，适合通过代码实践巩固理解。",
            },
        ]

        return {
            "agent": "ReviewPathAgent",
            "input": {
                "profile_student_id": profile.get("student_id"),
                "resource_count": len(resources),
            },
            "reviewed_resources": reviewed_resources,
            "learning_path": learning_path,
            "agent_log": "ReviewPathAgent 已完成 mock 资源审校，并生成个性化学习路径。",
        }

    def _review_report(self, profile: dict[str, Any]) -> dict[str, str]:
        return {
            "knowledge_grounding": "通过",
            "difficulty_match": "通过",
            "answer_consistency": "通过",
            "content_safety": "通过",
            "comment": f"资源难度已按 {profile.get('math_level', '未知')} 数学能力进行 mock 匹配。",
        }
