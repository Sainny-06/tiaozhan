from datetime import datetime
from typing import Any

from backend.agents.profile_agent import ProfileAgent
from backend.agents.resource_agent import ResourceAgent
from backend.agents.retrieval_agent import RetrievalAgent
from backend.agents.review_path_agent import ReviewPathAgent


class LearningPackageWorkflow:
    def __init__(self) -> None:
        self.profile_agent = ProfileAgent()
        self.retrieval_agent = RetrievalAgent()
        self.resource_agent = ResourceAgent()
        self.review_path_agent = ReviewPathAgent()

    def run(
        self,
        student_id: str,
        dialogue: str,
        target_course: str,
        target_topic: str,
    ) -> dict[str, Any]:
        task_id = f"task_{datetime.now().strftime('%Y%m%d%H%M%S')}"

        profile_result = self.profile_agent.build_profile(
            student_id=student_id,
            dialogue=dialogue,
        )
        retrieval_result = self.retrieval_agent.retrieve(
            profile=profile_result["profile"],
            target_topic=target_topic,
        )
        resource_result = self.resource_agent.generate_resources(
            profile=profile_result["profile"],
            retrieved_context=retrieval_result,
        )
        review_path_result = self.review_path_agent.review_and_plan(
            profile=profile_result["profile"],
            retrieved_context=retrieval_result,
            resources=resource_result["resources"],
        )

        return {
            "task_id": task_id,
            "status": "success",
            "target_course": target_course,
            "target_topic": target_topic,
            "profile_agent_output": profile_result,
            "retrieval_agent_output": retrieval_result,
            "resource_agent_output": resource_result,
            "review_path_agent_output": review_path_result,
            "resources": review_path_result["reviewed_resources"],
            "learning_path": review_path_result["learning_path"],
        }
