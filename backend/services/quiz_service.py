from typing import Any


class QuizService:
    def grade(self, package: dict[str, Any], answers: list[dict[str, str]]) -> dict[str, Any]:
        quiz = self._find_quiz(package)
        if not quiz:
            return {
                "ok": False,
                "error": "未找到 quiz 资源，无法评分。",
            }

        questions = quiz.get("questions", [])
        answer_map = {item["question_id"]: item.get("student_answer") for item in answers}
        analysis = []
        correct_count = 0

        for question in questions:
            question_id = question["question_id"]
            submitted = question_id in answer_map
            student_answer = answer_map.get(question_id) if submitted else "未作答"
            is_correct = submitted and student_answer == question.get("answer")

            if is_correct:
                correct_count += 1

            analysis.append(
                {
                    "question_id": question_id,
                    "knowledge_point": question.get("knowledge_point"),
                    "student_answer": student_answer,
                    "correct_answer": question.get("answer"),
                    "is_correct": is_correct,
                    "error_type": "" if is_correct else ("未作答" if not submitted else self._error_type(question)),
                    "explanation": question.get("explanation"),
                }
            )

        total_questions = len(questions)
        score = round(correct_count / total_questions * 100, 2) if total_questions else 0
        wrong_question_analysis = [item for item in analysis if not item["is_correct"]]
        wrong_points = []
        for item in wrong_question_analysis:
            point = item.get("knowledge_point")
            if point and point not in wrong_points:
                wrong_points.append(point)

        return {
            "ok": True,
            "score": score,
            "total_questions": total_questions,
            "correct_count": correct_count,
            "wrong_points": wrong_points,
            "wrong_question_analysis": wrong_question_analysis,
            "question_analysis": analysis,
        }

    def _find_quiz(self, package: dict[str, Any]) -> dict[str, Any] | None:
        for resource in package.get("resources", []):
            if resource.get("type") == "quiz":
                return resource
        return None

    def _error_type(self, question: dict[str, Any]) -> str:
        point = question.get("knowledge_point", "")
        if "代码" in point:
            return "代码实现理解错误"
        if "梯度" in point or "损失" in point:
            return "公式与优化理解错误"
        return "概念理解错误"
