from copy import deepcopy
from typing import Any


class ProfileAgent:
    def build_profile(self, student_id: str, dialogue: str) -> dict[str, Any]:
        profile = {
            "student_id": student_id,
            "major": "人工智能",
            "grade": "大二",
            "course": "机器学习基础",
            "learning_goal": "掌握目标章节并能完成代码实验",
            "knowledge_level": "中等偏弱",
            "math_level": "较弱",
            "coding_level": "较强",
            "cognitive_style": ["图解", "案例驱动", "代码实践"],
            "weak_points": ["Sigmoid 函数", "逻辑回归损失函数", "梯度下降"],
            "resource_preference": ["图解演示", "代码案例", "基础练习"],
            "mastery": {},
        }

        return {
            "agent": "ProfileAgent",
            "input": {
                "student_id": student_id,
                "dialogue": dialogue,
            },
            "profile": deepcopy(profile),
            "agent_log": "ProfileAgent 已从自然语言输入中生成 10 个画像维度的 mock 学生画像。",
        }

    def update_profile_after_quiz(
        self,
        old_profile: dict[str, Any],
        quiz_result: dict[str, Any],
    ) -> dict[str, Any]:
        new_profile = deepcopy(old_profile)
        wrong_points = quiz_result.get("wrong_points", [])
        wrong_analysis = quiz_result.get("wrong_question_analysis", [])
        correct_analysis = [
            item
            for item in quiz_result.get("question_analysis", [])
            if item.get("is_correct")
        ]
        profile_diff: list[dict[str, Any]] = []

        mastery = deepcopy(new_profile.get("mastery", {}))
        weak_points_before = list(new_profile.get("weak_points", []))
        weak_points_after = list(weak_points_before)

        for point in wrong_points:
            before = mastery.get(point, "未评估")
            mastery[point] = "低"
            if point not in weak_points_after:
                weak_points_after.append(point)
            profile_diff.append(
                {
                    "field": f"{point}掌握度",
                    "before": before,
                    "after": "低",
                    "reason": f"{point}相关题目答错",
                }
            )

        for item in correct_analysis:
            point = item.get("knowledge_point")
            if not point or point in wrong_points:
                continue
            before = mastery.get(point, "未评估")
            after = "较高" if before in {"未评估", "中", "低"} else before
            mastery[point] = after
            if before != after:
                profile_diff.append(
                    {
                        "field": f"{point}掌握度",
                        "before": before,
                        "after": after,
                        "reason": f"{point}相关题目答对",
                    }
                )

        new_profile["mastery"] = mastery
        new_profile["weak_points"] = weak_points_after

        if weak_points_after != weak_points_before:
            profile_diff.append(
                {
                    "field": "薄弱点",
                    "before": weak_points_before,
                    "after": weak_points_after,
                    "reason": "错题集中在相关知识点",
                }
            )

        code_wrong = any("代码" in point for point in wrong_points)
        code_correct = any(
            "代码" in (item.get("knowledge_point") or "")
            for item in correct_analysis
        )
        if code_correct and not code_wrong:
            new_profile["coding_level"] = old_profile.get("coding_level", "较强")

        return {
            "agent": "ProfileAgent",
            "profile_after": new_profile,
            "profile_diff": profile_diff,
            "agent_log": "ProfileAgent 已根据测验结果更新画像，并生成画像更新前后差异。",
        }
