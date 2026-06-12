# 恶意 WiFi 安全检测助手 (Malicious WiFi Detector MVP)

## 项目简介
基于 Agent-based 架构的 MVP，通过模拟分析 WiFi 网络特征，检测潜在的个人信息窃取风险，并向用户发出红/黄/绿灯直观安全预警。

**本项目为课程作业，所有数据均为本地模拟数据，不涉及真实网络扫描。**

## 版本
- **v4.0**（当前）：体验修复 — 对比区域始终可见、黑名单全风险等级开放、刷新持久化修复
- **v3.0**：新增黑名单备注、风险筛选计数、WiFi 对比分析功能
- **v2.0**：基于用户测试反馈迭代，新增风险排序/筛选、诊断原因标签、黑名单管理、用户反馈等功能
- **v1.0**：核心扫描→诊断→预警流程

## 快速开始

### 1. 创建虚拟环境（推荐）
```bash
python -m venv venv
```

### 2. 激活虚拟环境
- **Windows**: `venv\Scripts\activate`
- **macOS / Linux**: `source venv/bin/activate`

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

> **Windows 用户注意**：如果项目路径含中文字符，`pip` / `streamlit` 命令可能因路径编码问题失败。请改用：
> ```bash
> python -m pip install -r requirements.txt
> ```

### 4. 运行应用
```bash
streamlit run src/app.py
```

> **Windows 用户注意**：如遇同上编码问题，请改用：
> ```bash
> python -m streamlit run src/app.py
> ```

浏览器将自动打开 http://localhost:8501

## 使用说明

### 基础流程
1. 点击 **"📡 一键扫描周边 WiFi"** 按钮，加载模拟 WiFi 列表
2. WiFi 列表**按风险从高到低排列**，每条显示 🔴🟡🟢 风险图标、信号强度图标、加密方式
3. 筛选按钮显示各风险等级数量（如 "🔴 高风险 (2)"），快速感知区域安全态势
4. 存在同名 SSID 时显示 ⚠️同名 警告标记，已拉黑 WiFi 显示 🚫已拉黑 + 🏷备注标签
5. 可使用 **风险筛选按钮**（全部 / 🔴高风险 / 🟡中风险 / 🟢低风险）快速定位目标 WiFi
6. 选择 WiFi 后点击 **"🔍 开始诊断"** 查看详细报告

### 诊断报告
- **风险等级** + **诊断原因标签**（如 🔓开放网络、🕵️DNS劫持风险、🔗Portal认证）
- **意图分析**：模拟安全专家对攻击意图的判断
- **安全建议**：分级建议（紧急/注意/使用/保守）

### 黑名单与备注
- **任何风险等级的 WiFi** 诊断后均可填写 **2-5 字备注标签**（如"可疑热点"）并加入黑名单
- 已拉黑 WiFi 在列表中显示 🚫已拉黑 标记和 🏷备注标签
- 黑名单数据（列表 + 备注）持久化保存，**页面刷新后自动恢复**
- 可在黑名单管理区查看备注、移除黑名单，条目图标按实际风险等级显示

### WiFi 对比分析
- **未扫描时也可见**，显示引导提示"请先扫描周边 WiFi"
- 扫描后，可**选择两个 WiFi 进行并排对比**
- 从五个维度综合评估：风险等级、加密方式、信号强度、DNS 劫持风险、Portal 认证
- 对比结果包含：综合评分（满分 100，带差值指示）、五维度详细对比表（优胜方绿色高亮 ✅）
- 给出明确建议：🏆 建议连接 A / B / 两者安全性相当

### 用户反馈
- 展开底部反馈区，提交使用建议，数据保存至 `data/user_feedback.json`

## 项目结构
```
├── data/
│   ├── wifi_scenarios.json     # 模拟 WiFi 场景数据（8 个场景）
│   ├── user_feedback.json      # 用户反馈收集
│   └── blacklist_notes.json    # 黑名单备注持久化（v3.0）
├── docs/
│   ├── idea.md                 # 选题说明
│   ├── spec.md                 # 需求规格说明（整合 v1/v2/v3）
│   ├── plan.md                 # 技术方案（整合 v1/v2/v3）
│   └── tasks.md                # 任务拆解（整合 v1/v2/v3）
├── src/
│   ├── app.py                  # Streamlit 主程序入口（含对比分析）
│   ├── agent.py                # 模拟 AI Agent 推理、诊断、对比引擎
│   └── utils.py                # 数据加载、反馈保存、黑名单备注持久化
├── tests/                      # 用户测试反馈文档
├── .gitignore                  # 排除 .claude/、__pycache__/、venv/ 等
├── requirements.txt
├── README.md
├── CLAUDE.md
└── HANDOFF.md                  # 项目交接说明
```

## 技术栈
- Python 3.x + Streamlit (≥1.29.0)
- 规则引擎模拟 AI Agent 诊断（4 级规则 + 诊断原因标签）
- 五维度 WiFi 对比评分引擎（满分 100，含加密/信号/DNS/Portal 加权评分）
- 本地 JSON 数据驱动
