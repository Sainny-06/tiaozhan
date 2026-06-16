import json
import re
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

from backend.config import KNOWLEDGE_BASE_DIR


class CourseIndexService:
    def __init__(self, knowledge_base_dir: Path = KNOWLEDGE_BASE_DIR) -> None:
        self.knowledge_base_dir = knowledge_base_dir.resolve()
        self.index_path = (self.knowledge_base_dir / "index.json").resolve()

    def load_index(self) -> dict[str, Any]:
        with self.index_path.open("r", encoding="utf-8") as file:
            index = json.load(file)
        self.validate_index(index)
        return index

    def validate_index(self, index: dict[str, Any]) -> None:
        for chapter in index.get("chapters", []):
            self._resolve_chapter_path(chapter["file_path"])

    def get_index_summary(self) -> dict[str, Any]:
        index = self.load_index()
        return {
            "course_id": index.get("course_id"),
            "course_name": index.get("course_name"),
            "course_level": index.get("course_level"),
            "description": index.get("description"),
            "chapter_count": len(index.get("chapters", [])),
            "chapters": [
                {
                    "chapter_id": chapter.get("chapter_id"),
                    "title": chapter.get("title"),
                    "file_path": chapter.get("file_path"),
                    "difficulty": chapter.get("difficulty"),
                    "knowledge_points": [
                        item.get("name") for item in chapter.get("knowledge_points", [])
                    ],
                }
                for chapter in index.get("chapters", [])
            ],
        }

    def get_chapter(self, chapter_id: str) -> dict[str, Any]:
        index = self.load_index()
        chapter = next(
            (
                item
                for item in index.get("chapters", [])
                if item.get("chapter_id") == chapter_id
            ),
            None,
        )
        if not chapter:
            return {
                "found": False,
                "message": f"未找到 chapter_id={chapter_id} 的章节。",
            }

        content = self.read_chapter_markdown(chapter)
        return {
            "found": True,
            "chapter": chapter,
            "content": content,
            "sections": self.extract_sections(content),
        }

    def retrieve(self, target_topic: str) -> dict[str, Any]:
        index = self.load_index()
        chapters = index.get("chapters", [])
        matched_chapter, score = self._match_chapter(chapters, target_topic)

        if not matched_chapter or score < 0.25:
            return {
                "found": False,
                "message": f"未找到与“{target_topic}”匹配的课程章节。",
                "matched_chapter": None,
                "matched_knowledge_points": [],
                "source_refs": [],
                "retrieved_context": {
                    "chapter_title": None,
                    "content_preview": "",
                    "snippets": [],
                },
            }

        content = self.read_chapter_markdown(matched_chapter)
        sections = self.extract_sections(content)
        matched_points = [
            item.get("name")
            for item in matched_chapter.get("knowledge_points", [])
            if item.get("name")
        ]
        snippets = self._build_snippets(matched_points, sections, content)
        source_refs = [
            {
                "file": matched_chapter["file_path"],
                "section": snippet["section"],
                "reason": self._source_reason(matched_chapter["title"], snippet["section"]),
            }
            for snippet in snippets
        ]

        return {
            "found": True,
            "message": f"已匹配章节：{matched_chapter['title']}。",
            "matched_chapter": {
                "chapter_id": matched_chapter.get("chapter_id"),
                "title": matched_chapter.get("title"),
                "file_path": matched_chapter.get("file_path"),
                "difficulty": matched_chapter.get("difficulty"),
            },
            "matched_knowledge_points": matched_points,
            "source_refs": source_refs,
            "retrieved_context": {
                "chapter_title": matched_chapter.get("title"),
                "content_preview": self._preview(content),
                "snippets": snippets,
            },
        }

    def read_chapter_markdown(self, chapter: dict[str, Any]) -> str:
        path = self._resolve_chapter_path(chapter["file_path"])
        return path.read_text(encoding="utf-8")

    def extract_sections(self, content: str) -> dict[str, str]:
        sections: dict[str, str] = {}
        current_title: str | None = None
        current_lines: list[str] = []

        for line in content.splitlines():
            heading = re.match(r"^##\s+(.+?)\s*$", line)
            if heading:
                if current_title:
                    sections[current_title] = "\n".join(current_lines).strip()
                current_title = heading.group(1)
                current_lines = []
            elif current_title:
                current_lines.append(line)

        if current_title:
            sections[current_title] = "\n".join(current_lines).strip()
        return sections

    def _resolve_chapter_path(self, file_path: str) -> Path:
        if Path(file_path).is_absolute():
            raise ValueError("知识库 file_path 不能是绝对路径。")

        resolved = (self.knowledge_base_dir / file_path).resolve()
        if not resolved.is_relative_to(self.knowledge_base_dir):
            raise ValueError("检测到非法知识库路径穿越。")
        if not resolved.exists():
            raise FileNotFoundError(f"知识库文件不存在：{file_path}")
        return resolved

    def _match_chapter(
        self, chapters: list[dict[str, Any]], target_topic: str
    ) -> tuple[dict[str, Any] | None, float]:
        normalized_topic = self._normalize(target_topic)
        best: dict[str, Any] | None = None
        best_score = 0.0

        for chapter in chapters:
            candidates = [chapter.get("title", ""), chapter.get("file_path", "")]
            candidates.extend(
                point.get("name", "")
                for point in chapter.get("knowledge_points", [])
            )
            candidate_text = " ".join(candidates)
            normalized_candidate = self._normalize(candidate_text)

            score = SequenceMatcher(
                None, normalized_topic, normalized_candidate
            ).ratio()
            if normalized_topic and normalized_topic in normalized_candidate:
                score += 1.0
            for point in chapter.get("knowledge_points", []):
                point_name = self._normalize(point.get("name", ""))
                if point_name and (normalized_topic in point_name or point_name in normalized_topic):
                    score += 0.8

            if score > best_score:
                best = chapter
                best_score = score

        return best, best_score

    def _build_snippets(
        self,
        matched_points: list[str],
        sections: dict[str, str],
        content: str,
    ) -> list[dict[str, str]]:
        snippets: list[dict[str, str]] = []
        for point in matched_points:
            section_content = self._find_section_content(point, sections)
            if section_content:
                snippets.append(
                    {
                        "section": point,
                        "content": self._preview(section_content, max_length=260),
                    }
                )

        if not snippets:
            snippets.append(
                {
                    "section": "章节概览",
                    "content": self._preview(content, max_length=260),
                }
            )
        return snippets[:5]

    def _find_section_content(
        self, knowledge_point: str, sections: dict[str, str]
    ) -> str | None:
        normalized_point = self._normalize(knowledge_point)
        for title, content in sections.items():
            normalized_title = self._normalize(title)
            if normalized_point in normalized_title or normalized_title in normalized_point:
                return content

        for title, content in sections.items():
            normalized_content = self._normalize(content)
            if normalized_point in normalized_content:
                return content
        return None

    def _source_reason(self, chapter_title: str, section: str) -> str:
        reason_map = {
            "Sigmoid 函数": "用于解释逻辑回归如何将线性输出映射为概率。",
            "逻辑回归损失函数": "用于说明分类任务中预测概率与真实标签的误差度量。",
            "梯度下降优化": "用于说明模型参数如何通过迭代更新降低损失。",
            "线性模型": "用于说明线性回归如何用特征加权和预测连续值。",
            "最小二乘法": "用于说明线性回归如何最小化平方误差。",
            "梯度下降": "用于说明线性回归参数的迭代优化方式。",
        }
        return reason_map.get(section, f"来自《{chapter_title}》章节，用于支撑“{section}”相关资源生成。")

    def _preview(self, content: str, max_length: int = 320) -> str:
        compact = re.sub(r"\s+", " ", content).strip()
        if len(compact) <= max_length:
            return compact
        return compact[:max_length].rstrip() + "..."

    def _normalize(self, value: str) -> str:
        return re.sub(r"\s+", "", value or "").lower()
