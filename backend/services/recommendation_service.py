from typing import Any


class RecommendationService:
    def generate(
        self,
        wrong_points: list[str],
        topic: str,
    ) -> dict[str, list[dict[str, Any]]]:
        if not wrong_points:
            recommendations = [
                {
                    "title": f"{topic}进阶代码实验",
                    "type": "code_lab",
                    "reason": "测验表现较好，建议通过更完整的代码实验进行迁移应用。",
                },
                {
                    "title": f"{topic}综合项目挑战",
                    "type": "project",
                    "reason": "当前薄弱点较少，可进入综合任务巩固模型流程。",
                },
            ]
            return {
                "new_recommendations": recommendations,
                "updated_learning_path": [
                    {
                        "step": 1,
                        "title": f"完成{topic}进阶代码实验",
                        "recommended_resources": [recommendations[0]["title"]],
                        "reason": "学生已完成基础测验，适合进入实践提升。",
                    },
                    {
                        "step": 2,
                        "title": f"完成{topic}综合项目挑战",
                        "recommended_resources": [recommendations[1]["title"]],
                        "reason": "通过综合项目检验迁移应用能力。",
                    },
                ],
            }

        recommendations: list[dict[str, Any]] = []
        path: list[dict[str, Any]] = []

        for point in wrong_points:
            for item in self._recommendations_for_point(point):
                if item["title"] not in {existing["title"] for existing in recommendations}:
                    recommendations.append(item)

        for index, item in enumerate(recommendations, start=1):
            path.append(
                {
                    "step": index,
                    "title": f"补充学习 {item['title']}",
                    "recommended_resources": [item["title"]],
                    "reason": item["reason"],
                }
            )

        return {
            "new_recommendations": recommendations,
            "updated_learning_path": path,
        }

    def _recommendations_for_point(self, point: str) -> list[dict[str, str]]:
        mapping = {
            "Sigmoid 函数": [
                {
                    "title": "Sigmoid 函数图解演示",
                    "type": "animation",
                    "reason": "学生在 Sigmoid 函数题目中答错，建议先通过图解理解概率映射。",
                },
                {
                    "title": "Sigmoid 基础专项练习",
                    "type": "quiz",
                    "reason": "通过低难度题目巩固 Sigmoid 输出范围和概率含义。",
                },
            ],
            "逻辑回归损失函数": [
                {
                    "title": "逻辑回归损失函数专项讲义",
                    "type": "lecture",
                    "reason": "学生对损失函数公式含义掌握不足。",
                },
                {
                    "title": "损失函数公式拆解练习",
                    "type": "quiz",
                    "reason": "通过公式拆解练习理解交叉熵惩罚机制。",
                },
            ],
            "梯度下降优化": [
                {
                    "title": "梯度下降步骤图解",
                    "type": "animation",
                    "reason": "学生对参数更新方向和学习率作用理解不足。",
                },
                {
                    "title": "梯度下降基础练习",
                    "type": "quiz",
                    "reason": "通过基础题巩固负梯度方向和迭代更新概念。",
                },
            ],
        }
        return mapping.get(
            point,
            [
                {
                    "title": f"{point}专项复习资源",
                    "type": "lecture",
                    "reason": f"学生在“{point}”相关题目中答错，建议补充专项复习。",
                }
            ],
        )
