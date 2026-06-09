# 恶意 WiFi 安全检测助手 (Malicious WiFi Detector MVP)

## 项目简介
基于 Agent-based 架构的 MVP，通过模拟分析 WiFi 网络特征，检测潜在的个人信息窃取风险，并向用户发出红/黄/绿灯直观安全预警。

**本项目为课程作业，所有数据均为本地模拟数据，不涉及真实网络扫描。**

## 版本
- **v2.0**（当前）：基于用户测试反馈迭代，新增风险排序/筛选、诊断原因标签、黑名单管理、用户反馈等功能
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

### 4. 运行应用
```bash
streamlit run src/app.py
```

浏览器将自动打开 http://localhost:8501

## 使用说明

### 基础流程
1. 点击 **"📡 一键扫描周边 WiFi"** 按钮，加载模拟 WiFi 列表
2. WiFi 列表**按风险从高到低排列**，每条显示 🔴🟡🟢 风险图标、信号强度图标、加密方式
3. 存在同名 SSID 时显示 ⚠️同名 警告标记
4. 可使用 **风险筛选按钮**（全部 / 🔴高风险 / 🟡中风险 / 🟢低风险）快速定位目标 WiFi
5. 选择 WiFi 后点击 **"🔍 开始诊断"** 查看详细报告

### 诊断报告
- **风险等级** + **诊断原因标签**（如 🔓开放网络、🕵️DNS劫持风险、🔗Portal认证）
- **意图分析**：模拟安全专家对攻击意图的判断
- **安全建议**：分级建议（紧急/注意/使用/保守）

### 高级功能
- **黑名单**：高风险 WiFi 可加入黑名单，在页面统一管理
- **用户反馈**：展开底部反馈区，提交使用建议

## 项目结构
```
├── data/
│   ├── wifi_scenarios.json     # 模拟 WiFi 场景数据（8 个场景）
│   └── user_feedback.json      # 用户反馈收集
├── docs/
│   ├── idea.md                 # 选题说明
│   ├── spec_v1.md / spec_v2.md # 需求规格说明
│   ├── plan_v1.md / plan_v2.md # 技术方案
│   └── tasks_v1.md / tasks_v2.md # 任务拆解
├── src/
│   ├── app.py                  # Streamlit 主程序入口
│   ├── agent.py                # 模拟 AI Agent 推理与诊断逻辑
│   └── utils.py                # 数据加载、反馈保存工具
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
- 本地 JSON 数据驱动
