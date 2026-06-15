from copy import deepcopy
from typing import Any


class ProfileAgent:
    def build_profile(self, student_id: str, dialogue: str) -> dict[str, Any]:
        profile = {
            "student_id": student_id,
            "major": "人工智能",
            "grade": "大二",
            "course": "机器学习基础",
            "learning_goal": "掌握逻辑回归并能完成代码实验",
            "knowledge_level": "中等偏弱",
            "math_level": "较弱",
            "coding_level": "较强",
            "cognitive_style": ["图解", "案例驱动", "代码实践"],
            "weak_points": ["Sigmoid 函数", "逻辑回归损失函数", "梯度下降"],
            "resource_preference": ["图解演示", "代码案例", "基础练习"],
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
