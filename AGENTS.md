# AGENTS.md

## 项目背景

本项目是第十五届中国软件杯 A3 赛题的最小 MVP：  
“基于大模型的个性化资源生成与学习多智能体系统”。

请优先阅读 `docs/MVP.MD`，所有功能、目录、接口、数据结构、Agent 设计都以该文档为准。

## 开发目标

先实现一个可运行的 MVP，而不是追求复杂完整系统。

MVP 必须完成以下闭环：

1. 学生通过自然语言输入学习需求；
2. 后端 Profile Agent 构建学生画像；
3. Retrieval Agent 基于 `knowledge_base/index.json` 检索课程知识库；
4. Resource Agent 生成 5 类个性化资源：
   - 个性化讲义；
   - Mermaid 思维导图；
   - 分层题库；
   - Python 代码实操；
   - 轻量动画 / 图解演示；
5. ReviewPath Agent 为每个资源生成来源依据、审校报告和学习路径；
6. 学生完成测验后展示画像更新前后对比；
7. 系统根据测验结果生成新增推荐资源和调整后的学习路径。

## 技术要求

后端优先使用：

- Python
- FastAPI
- SQLite
- Pydantic
- 本地 Markdown 知识库
- 模拟 LLM 服务，先不强依赖真实大模型 API

前端优先使用：

- Vue 3
- Vite
- Element Plus 或其他轻量 UI 库
- Markdown 渲染
- Mermaid 渲染

## 重要约束

1. 不要先接真实大模型 API。
2. 第一阶段先用 mock LLM，让系统可以本地完整跑通。
3. 后端必须真实存在 4 个 Agent 模块：
   - `profile_agent.py`
   - `retrieval_agent.py`
   - `resource_agent.py`
   - `review_path_agent.py`
4. 前端 Agent 执行日志必须来自后端真实输出，不能写死。
5. 每个资源必须包含：
   - `source_refs`
   - `review_report`
6. 知识库必须包含：
   - `knowledge_base/index.json`
   - 至少 10 个课程 Markdown 文件
7. 测验提交后必须返回：
   - `profile_before`
   - `profile_after`
   - `profile_diff`
   - `wrong_points`
   - `new_recommendations`
   - `updated_learning_path`

## 开发顺序

请严格按阶段开发：

1. 搭建后端目录和 FastAPI 基础服务；
2. 实现知识库和 index.json；
3. 实现 4 个真实 Agent；
4. 实现资源包生成接口；
5. 实现测验提交和画像更新接口；
6. 再搭建前端页面；
7. 最后做 UI 美化和演示数据。

## 验收标准

每完成一个阶段，请运行项目并说明：

1. 新增了哪些文件；
2. 修改了哪些文件；
3. 如何启动；
4. 如何测试；
5. 是否满足 `docs/MVP.MD` 中对应要求。

不要一次性生成大量不可运行代码。每次完成一个可验证的小阶段。