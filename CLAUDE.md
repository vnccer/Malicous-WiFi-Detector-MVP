# 恶意 WiFi 检测 MVP v2.0 (Malicious WiFi Detector MVP)

## 1. 项目简介与目标
本项目是一个基于 Agent-based 的 MVP（最小可行性产品），属于课程作业。
核心目标是：通过模拟分析 WiFi 网络特征，检测潜在的个人信息窃取风险，并向用户发出直观的安全预警（红/黄/绿灯指示）。
**注意：本项目重点在于"结构化 Vibe Coding"和跑通核心业务流程，绝不涉及真实的底层网络流量抓包或真实的复杂大模型调用。**

### v2.0 迭代要点（基于用户测试反馈）
- 同名 SSID 检测与 MAC 地址唯一标识，防止恶意热点伪装覆盖
- 风险排序（高→低）+ 筛选按钮（全部/高/中/低）
- 信号强度真实 dBm 显示 + 分级图标（优秀/良好/较弱）
- 显式「开始诊断」按钮，选择与诊断解耦
- 诊断原因标签（彩色 pill），增强视觉直观性
- 黑名单管理功能
- 用户反馈收集（保存至 `data/user_feedback.json`）

## 2. 技术栈与架构
- **前端交互/UI**: Python + Streamlit (使用 `st.container(border=True)` 卡片布局)
- **核心逻辑 (Agent)**: Python (通过预设规则表 + `_build_reasons()` 诊断标签，模拟安全专家的 Prompt 意图识别，生成结构化诊断报告)
- **数据层**: 本地 JSON 文件 (`wifi_scenarios.json`) 模拟真实场景（如咖啡厅、机场等）的 WiFi 特征。WiFi 唯一标识使用 MAC 地址，避免同名 SSID 覆盖。

## 3. 目录结构规范
请严格按照以下目录结构读取和生成文件：

malicous-wifi-detector-mvp/
├── data/
│   ├── wifi_scenarios.json     # 模拟 WiFi 场景数据（8 个场景，含同名伪造）
│   └── user_feedback.json      # 用户反馈收集（v2.0 新增）
├── docs/
│   ├── idea.md                 # 选题背景与动机说明
│   ├── spec_v1.md / spec_v2.md # 需求说明：用户、功能、验收标准和边界
│   ├── plan_v1.md / plan_v2.md # 技术方案、页面结构、数据流草图
│   └── tasks_v1.md / tasks_v2.md # 拆解的开发任务（v1 保留，v2 为当前版本）
├── src/
│   ├── app.py                  # Streamlit 主程序入口（含排序/筛选/黑名单/反馈）
│   ├── agent.py                # 模拟 AI Agent 推理与诊断逻辑（含 diagnosis_reasons）
│   └── utils.py                # 数据加载与反馈保存工具函数
├── tests/                      # 用户测试反馈文档
├── .gitignore                  # 排除 .claude/、__pycache__/、venv/、用户反馈等
├── README.md                   # 项目安装、运行、使用说明
├── HANDOFF.md                  # 项目交接说明（角色分工）
└── CLAUDE.md                   # AI 助手全局系统指令（本文件）

## 4. AI 助手开发准则 (Critical Rules)

### 4.1 绝对的 MVP 边界限制
- **禁止网络抓包：** 绝对不要引入 scapy, pcap 或任何尝试获取宿主机真实 WiFi 列表的代码。所有数据必须来自 `data/wifi_scenarios.json`。
- **模拟大模型：** 不要引入 openai, langchain 等重量级库。只需在 `src/agent.py` 中写一个函数，接收 JSON 字典，通过 if/else 规则映射返回包含 `risk_level`、`intent_analysis`、`security_advice`、`diagnosis_reasons` 的字典来模拟 LLM 输出即可。

### 4.2 遵循 SDD/TDD 流程
- 在开始编写 `src/` 下的代码前，必须先确认 `docs/spec_v2.md`, `docs/plan_v2.md`, `docs/tasks_v2.md` 中有相应的规划。
- 遵循最小验证方案：开发功能时，需考虑 1 个核心成功路径、2-3 个边界情况和 1 个失败场景（例如 JSON 数据缺失或格式错误）。

### 4.3 关键架构约束
- **WiFi 唯一标识**：必须使用 `get_wifi_uid()` 基于 MAC 地址生成，不得用 SSID 做 key（会覆盖同名热点）。
- **信号显示**：信号强度显示真实负值 dBm，不使用 abs()。
- **风险卡片**：使用 `st.container(border=True)`，不要使用 `st.error/warning/success` 上下文管理器（已知 bug：仅渲染最后子元素）。
- **诊断输出**：agent 返回的字典必须包含 4 个字段：`risk_level`、`intent_analysis`、`security_advice`、`diagnosis_reasons`。

### 4.4 配合生成课程报告所需的记录
- 课程要求保留"关键提示词、AI生成内容、遇到问题及人工修改"。
- 当你（AI）帮我完成一个复杂逻辑后，请在输出总结时，简要提供一段**"AI 辅助开发记录备忘"**（例如："本次使用了XX提示词，生成了XX代码，解决了XX报错"），以便我们小组的成员摘录进 PPT 和最终报告中。

### 4.5 语言规范
- **保持中文：** 所有生成的代码注释、控制台输出日志、以及前端 Streamlit 向用户展示的界面文本内容，必须全程保持中文。

## 5. 常用命令
- **创建虚拟环境**：`python -m venv venv` (或 `python3 -m venv venv`)
- **激活虚拟环境**：
  - Windows 侧: `venv\Scripts\activate`
  - macOS/Linux 侧: `source venv/bin/activate`
- **安装依赖**：`pip install -r requirements.txt` (仅需 streamlit >= 1.29.0)
- **运行应用**：`streamlit run src/app.py`
