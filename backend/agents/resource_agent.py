from typing import Any


class ResourceAgent:
    def generate_resources(
        self,
        profile: dict[str, Any],
        retrieved_context: dict[str, Any],
        target_topic: str | None = None,
    ) -> dict[str, Any]:
        source_refs = retrieved_context.get("source_refs", [])
        context = retrieved_context.get("retrieved_context", {})
        matched_chapter = retrieved_context.get("matched_chapter") or {}
        topic = matched_chapter.get("title") or target_topic or "未匹配主题"
        weak_points = "、".join(profile.get("weak_points", [])) or "当前薄弱点"
        snippets = context.get("snippets", [])
        key_points = [item.get("section") for item in snippets if item.get("section")]
        if not key_points:
            key_points = retrieved_context.get("matched_knowledge_points", []) or [topic]

        resources = [
            {
                "type": "lecture",
                "title": f"面向当前学生画像的{topic}个性化讲义",
                "content": (
                    f"本讲义围绕“{topic}”展开，结合学生薄弱点：{weak_points}。"
                    f"核心参考片段包括：{'、'.join(key_points[:3])}。"
                ),
                "source_refs": source_refs,
                "review_report": self._mock_review("lecture", source_refs),
            },
            {
                "type": "mindmap",
                "title": f"{topic}知识结构图",
                "mermaid_code": self._mindmap(topic, key_points),
                "source_refs": source_refs,
                "review_report": self._mock_review("mindmap", source_refs),
            },
            {
                "type": "quiz",
                "title": f"{topic}分层练习题",
                "questions": self._quiz(topic),
                "source_refs": source_refs,
                "review_report": self._mock_review("quiz", source_refs),
            },
            {
                "type": "code_lab",
                "title": f"使用 Python 实践{topic}",
                "code": self._code_lab(topic),
                "source_refs": source_refs,
                "review_report": self._mock_review("code_lab", source_refs),
            },
            {
                "type": "animation",
                "title": f"{topic}轻量图解演示",
                "steps": ["观察问题", "建立模型", "计算损失", "优化参数", "输出结果"],
                "mermaid_code": self._flow(topic, key_points),
                "source_refs": source_refs,
                "review_report": self._mock_review("animation", source_refs),
            },
        ]

        return {
            "agent": "ResourceAgent",
            "input": {
                "profile_student_id": profile.get("student_id"),
                "target_topic": target_topic,
                "matched_chapter": matched_chapter,
                "source_ref_count": len(source_refs),
            },
            "resources": resources,
            "agent_log": (
                f"ResourceAgent 已基于 RetrievalAgent 返回的真实 source_refs "
                f"为“{topic}”生成 5 类 mock 资源，其中 quiz 为结构化题目。"
            ),
        }

    def _mock_review(
        self, resource_type: str, source_refs: list[dict[str, Any]]
    ) -> dict[str, str]:
        grounded = bool(source_refs)
        answer_consistency = "通过" if resource_type == "quiz" else "不适用"
        return {
            "knowledge_grounding": "通过" if grounded else "待补充",
            "difficulty_match": "通过",
            "answer_consistency": answer_consistency,
            "content_safety": "通过",
            "comment": (
                "资源已绑定真实知识库来源。"
                if grounded
                else "当前资源缺少知识库来源依据，需补充 source_refs。"
            ),
        }

    def _mindmap(self, topic: str, key_points: list[str]) -> str:
        children = "\n".join(f"    {point}" for point in key_points[:5])
        return f"mindmap\n  root(({topic}))\n{children}"

    def _quiz(self, topic: str) -> list[dict[str, Any]]:
        if "逻辑回归" in topic:
            return [
                {
                    "question_id": "q_logistic_idea_001",
                    "question_type": "single_choice",
                    "question": "逻辑回归主要用于解决哪类机器学习任务？",
                    "options": {
                        "A": "二分类或分类概率预测",
                        "B": "只预测连续房价",
                        "C": "只做无监督聚类",
                        "D": "只做图像生成",
                    },
                    "answer": "A",
                    "explanation": "逻辑回归通常用于分类任务，输出样本属于正类的概率。",
                    "knowledge_point": "分类问题与逻辑回归思想",
                    "difficulty": "easy",
                },
                {
                    "question_id": "q_logistic_sigmoid_001",
                    "question_type": "single_choice",
                    "question": "Sigmoid 函数的输出范围是？",
                    "options": {
                        "A": "0 到 1",
                        "B": "-1 到 1",
                        "C": "任意实数",
                        "D": "只能是 0 或 1",
                    },
                    "answer": "A",
                    "explanation": "Sigmoid 函数会将任意实数映射到 0 到 1 之间，常用于表示概率。",
                    "knowledge_point": "Sigmoid 函数",
                    "difficulty": "easy",
                },
                {
                    "question_id": "q_logistic_loss_001",
                    "question_type": "single_choice",
                    "question": "逻辑回归常用的损失函数是？",
                    "options": {
                        "A": "均方误差",
                        "B": "交叉熵损失",
                        "C": "欧氏距离",
                        "D": "信息增益",
                    },
                    "answer": "B",
                    "explanation": "交叉熵损失适合衡量概率预测与真实二分类标签之间的差异。",
                    "knowledge_point": "逻辑回归损失函数",
                    "difficulty": "medium",
                },
                {
                    "question_id": "q_logistic_gradient_001",
                    "question_type": "single_choice",
                    "question": "梯度下降优化中，参数通常沿什么方向更新？",
                    "options": {
                        "A": "梯度方向",
                        "B": "负梯度方向",
                        "C": "随机固定方向",
                        "D": "损失最大的样本方向",
                    },
                    "answer": "B",
                    "explanation": "梯度表示损失上升最快方向，沿负梯度方向更新可降低损失。",
                    "knowledge_point": "梯度下降优化",
                    "difficulty": "medium",
                },
                {
                    "question_id": "q_logistic_code_001",
                    "question_type": "single_choice",
                    "question": "用 NumPy 实现逻辑回归时，通常首先需要实现哪个函数？",
                    "options": {
                        "A": "sigmoid",
                        "B": "softmax for text generation",
                        "C": "kmeans",
                        "D": "decision_tree_split",
                    },
                    "answer": "A",
                    "explanation": "逻辑回归需要用 sigmoid 将线性输出转换为概率。",
                    "knowledge_point": "逻辑回归代码实现",
                    "difficulty": "medium",
                },
            ]

        if "线性回归" in topic:
            return [
                {
                    "question_id": "q_linear_model_001",
                    "question_type": "single_choice",
                    "question": "线性回归中的线性模型主要表达什么关系？",
                    "options": {
                        "A": "特征加权和与连续目标之间的关系",
                        "B": "样本之间的最近邻关系",
                        "C": "类别之间的树状关系",
                        "D": "文本生成概率",
                    },
                    "answer": "A",
                    "explanation": "线性模型使用特征的加权和预测连续数值目标。",
                    "knowledge_point": "线性模型",
                    "difficulty": "easy",
                },
                {
                    "question_id": "q_linear_least_squares_001",
                    "question_type": "single_choice",
                    "question": "最小二乘法希望最小化什么？",
                    "options": {
                        "A": "预测误差平方和",
                        "B": "分类交叉熵",
                        "C": "样本数量",
                        "D": "特征维度",
                    },
                    "answer": "A",
                    "explanation": "最小二乘法通过最小化预测值与真实值的平方误差来估计参数。",
                    "knowledge_point": "最小二乘法",
                    "difficulty": "medium",
                },
                {
                    "question_id": "q_linear_loss_001",
                    "question_type": "single_choice",
                    "question": "线性回归中常用的损失函数是？",
                    "options": {
                        "A": "均方误差",
                        "B": "信息增益",
                        "C": "基尼指数",
                        "D": "Sigmoid 函数",
                    },
                    "answer": "A",
                    "explanation": "均方误差适合衡量连续数值预测与真实值之间的差异。",
                    "knowledge_point": "损失函数",
                    "difficulty": "easy",
                },
                {
                    "question_id": "q_linear_gradient_001",
                    "question_type": "single_choice",
                    "question": "线性回归使用梯度下降时，学习率控制什么？",
                    "options": {
                        "A": "参数每次更新的步长",
                        "B": "训练集样本数量",
                        "C": "测试集标签",
                        "D": "特征名称",
                    },
                    "answer": "A",
                    "explanation": "学习率决定沿负梯度方向更新参数时每一步走多远。",
                    "knowledge_point": "梯度下降",
                    "difficulty": "medium",
                },
                {
                    "question_id": "q_linear_code_001",
                    "question_type": "single_choice",
                    "question": "NumPy 中 X @ w + b 常用于表示什么？",
                    "options": {
                        "A": "线性回归预测值",
                        "B": "KNN 距离",
                        "C": "决策树剪枝",
                        "D": "交叉验证折数",
                    },
                    "answer": "A",
                    "explanation": "X @ w + b 是多变量线性回归预测函数的常见向量化写法。",
                    "knowledge_point": "线性回归代码实现",
                    "difficulty": "medium",
                },
            ]

        return [
            {
                "question_id": "q_general_001",
                "question_type": "single_choice",
                "question": f"当前主题“{topic}”尚未匹配课程章节，应优先做什么？",
                "options": {
                    "A": "补充知识库章节和索引",
                    "B": "忽略来源依据",
                    "C": "删除测验",
                    "D": "直接接入真实大模型",
                },
                "answer": "A",
                "explanation": "未匹配主题需要先补充课程知识库，保证资源有来源依据。",
                "knowledge_point": topic,
                "difficulty": "easy",
            }
        ]

    def _code_lab(self, topic: str) -> str:
        if "逻辑回归" in topic:
            return (
                "import numpy as np\n\n"
                "def sigmoid(z):\n"
                "    return 1 / (1 + np.exp(-z))\n\n"
                "# 后续可加入交叉熵损失和梯度下降更新\n"
            )
        if "线性回归" in topic:
            return (
                "import numpy as np\n\n"
                "def predict(X, w, b):\n"
                "    return X @ w + b\n\n"
                "def mse(y_true, y_pred):\n"
                "    return np.mean((y_true - y_pred) ** 2)\n"
            )
        return "# 当前主题暂未匹配专用代码模板，可根据检索片段补充实践代码。\n"

    def _flow(self, topic: str, key_points: list[str]) -> str:
        first = key_points[0] if key_points else "核心概念"
        second = key_points[1] if len(key_points) > 1 else "模型训练"
        return (
            "flowchart LR\n"
            f"  A[{topic}] --> B[{first}]\n"
            f"  B --> C[{second}]\n"
            "  C --> D[练习与实践]\n"
        )
