from typing import Any


class ResourceAgent:
    def generate_resources(
        self,
        profile: dict[str, Any],
        retrieved_context: dict[str, Any],
    ) -> dict[str, Any]:
        source_refs = retrieved_context.get("source_refs", [])
        weak_points = "、".join(profile.get("weak_points", []))

        resources = [
            {
                "type": "lecture",
                "title": "面向数学基础较弱学生的逻辑回归通俗讲义",
                "content": f"围绕 {weak_points}，用概率、图解和例子解释逻辑回归。",
                "source_refs": source_refs,
                "review_report": self._mock_review("lecture"),
            },
            {
                "type": "mindmap",
                "title": "逻辑回归知识结构图",
                "mermaid_code": "mindmap\n  root((逻辑回归))\n    分类问题\n    Sigmoid函数\n    损失函数\n    梯度下降\n    Python实现",
                "source_refs": source_refs,
                "review_report": self._mock_review("mindmap"),
            },
            {
                "type": "quiz",
                "title": "逻辑回归分层练习题",
                "questions": [
                    {
                        "id": "q_001",
                        "level": "基础",
                        "knowledge_point": "Sigmoid 函数",
                        "question": "Sigmoid 函数的输出范围是什么？",
                        "answer": "0 到 1",
                    },
                    {
                        "id": "q_002",
                        "level": "理解",
                        "knowledge_point": "逻辑回归损失函数",
                        "question": "为什么逻辑回归常用交叉熵损失？",
                        "answer": "它适合衡量概率预测与真实二分类标签之间的差异。",
                    },
                ],
                "source_refs": source_refs,
                "review_report": self._mock_review("quiz"),
            },
            {
                "type": "code_lab",
                "title": "使用 Python 实现逻辑回归分类",
                "code": "import numpy as np\n\ndef sigmoid(z):\n    return 1 / (1 + np.exp(-z))\n",
                "source_refs": source_refs,
                "review_report": self._mock_review("code_lab"),
            },
            {
                "type": "animation",
                "title": "Sigmoid 概率映射轻量图解演示",
                "steps": ["输入特征", "线性组合", "Sigmoid 映射", "输出分类概率"],
                "mermaid_code": "flowchart LR\n  A[输入特征] --> B[线性组合 z]\n  B --> C[Sigmoid 函数]\n  C --> D[概率输出]",
                "source_refs": source_refs,
                "review_report": self._mock_review("animation"),
            },
        ]

        return {
            "agent": "ResourceAgent",
            "input": {
                "profile_student_id": profile.get("student_id"),
                "matched_chapter": retrieved_context.get("matched_chapter"),
            },
            "resources": resources,
            "agent_log": "ResourceAgent 已生成 5 类 mock 个性化资源，且每个资源包含 source_refs 与 review_report。",
        }

    def _mock_review(self, resource_type: str) -> dict[str, str]:
        answer_consistency = "通过" if resource_type == "quiz" else "不适用"
        return {
            "knowledge_grounding": "通过",
            "difficulty_match": "通过",
            "answer_consistency": answer_consistency,
            "content_safety": "通过",
            "comment": "第一阶段 mock 审校：资源基于检索来源生成，难度匹配学生画像。",
        }
