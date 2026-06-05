# 恶意 WiFi 检测 MVP (Malicious WiFi Detector MVP)

## 1. 项目简介与目标
本项目是一个基于 Agent-based 的 MVP（最小可行性产品），属于课程作业。
核心目标是：通过模拟分析 WiFi 网络特征，检测潜在的个人信息窃取风险，并向用户发出直观的安全预警（红/黄/绿灯指示）。
**注意：本项目重点在于“结构化 Vibe Coding”和跑通核心业务流程，绝不涉及真实的底层网络流量抓包或真实的复杂大模型调用。**

## 2. 技术栈与架构
- **前端交互/UI**: Python + Streamlit (提供一键扫描交互和视觉卡片展示)
- **核心逻辑 (Agent)**: Python (通过静态映射表和预设规则，模拟安全专家的 Prompt 意图识别，生成结构化诊断报告)
- **数据层**: 本地 JSON 文件 (`wifi_scenarios.json`) 模拟真实场景（如咖啡厅、机场等）的 WiFi 特征。

## 3. 目录结构规范
请严格按照以下目录结构读取和生成文件：

malicous-wifi-detector-mvp/
├── data/
│   └── wifi_scenarios.json   # 必须从这里读取模拟的 WiFi 场景数据，不要自动生成网络请求
├── docs/
│   ├── spec.md               # 需求说明：用户、功能、验收标准和边界
│   ├── plan.md               # 技术方案、页面结构、数据流草图
│   └── tasks.md              # 拆解的 30-60 分钟开发小任务
├── src/
│   ├── app.py                # Streamlit 主程序入口
│   ├── agent.py              # 模拟 AI Agent 推理与诊断逻辑
│   └── utils.py              # 数据加载与辅助工具函数
├── tests/                    # (可选) 用于最小 TDD 验证的测试脚本
├── README.md                 # 项目安装、运行、测试和 demo 步骤说明
└── CLAUDE.md                 # AI 助手全局系统指令（本文件）

## 4. AI 助手开发准则 (Critical Rules)

### 4.1 绝对的 MVP 边界限制
- **禁止网络抓包：** 绝对不要引入 scapy, pcap 或任何尝试获取宿主机真实 WiFi 列表的代码。所有数据必须来自 `data/wifi_scenarios.json`。
- **模拟大模型：** 不要引入 openai, langchain 等重量级库。只需在 `src/agent.py` 中写一个函数，接收 JSON 字典，通过 if/else 或字典映射返回包含“风险等级(High/Med/Low)、意图识别、建议”的字典来模拟 LLM 输出即可。

### 4.2 遵循 SDD/TDD 流程
- 在开始编写 `src/` 下的代码前，必须先确认 `docs/spec.md`, `docs/plan.md`, `docs/tasks.md` 中有相应的规划。
- 遵循最小验证方案：开发功能时，需考虑 1 个核心成功路径、2-3 个边界情况和 1 个失败场景（例如 JSON 数据缺失或格式错误）。

### 4.3 配合生成课程报告所需的记录
- 课程要求保留“关键提示词、AI生成内容、遇到问题及人工修改”。
- 当你（AI）帮我完成一个复杂逻辑后，请在输出总结时，简要提供一段**“AI 辅助开发记录备忘”**（例如：“本次使用了XX提示词，生成了XX代码，解决了XX报错”），以便我们小组的成员摘录进 PPT 和最终报告中。

### 4.4 语言规范
- **保持中文：** 所有生成的代码注释、控制台输出日志、以及前端 Streamlit 向用户展示的界面文本内容，必须全程保持中文。

## 5. 常用命令
- **创建虚拟环境**：`python -m venv venv` (或 `python3 -m venv venv`)
- **激活虚拟环境**：
  - Windows 侧: `venv\Scripts\activate`
  - macOS/Linux 侧: `source venv/bin/activate`
- **安装依赖**：`pip install -r requirements.txt` (预计仅需 streamlit)
- **运行应用**：`streamlit run src/app.py`