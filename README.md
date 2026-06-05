# 恶意 WiFi 安全检测助手 (Malicious WiFi Detector MVP)

## 项目简介
基于 Agent-based 架构的 MVP，通过模拟分析 WiFi 网络特征，检测潜在的个人信息窃取风险，并向用户发出红/黄/绿灯直观安全预警。

**本项目为课程作业，所有数据均为本地模拟数据，不涉及真实网络扫描。**

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
1. 点击 **"一键扫描周边 WiFi"** 按钮
2. 在 WiFi 列表中选择一个网络进行诊断
3. 查看红/黄/绿灯安全分析报告

## 项目结构
```
├── data/wifi_scenarios.json   # 模拟 WiFi 场景数据
├── docs/                      # 需求、方案、任务文档
├── src/
│   ├── app.py                 # Streamlit 主程序
│   ├── agent.py               # 模拟 AI Agent 推理
│   └── utils.py               # 数据加载工具
├── requirements.txt
└── README.md
```

## 技术栈
- Python 3.x + Streamlit
- 规则引擎模拟 AI Agent 诊断
- 本地 JSON 数据驱动
