# 恶意 WiFi 检测 MVP — 技术方案

## 技术栈
- **前端/UI**: Python + Streamlit
- **核心逻辑**: Python 规则引擎（模拟 AI Agent）
- **数据层**: 本地 JSON 文件

## 目录结构
```
├── data/wifi_scenarios.json   # 模拟 WiFi 场景数据
├── docs/spec.md               # 需求说明
├── docs/plan.md               # 本文件 — 技术方案
├── docs/tasks.md              # 任务拆解
├── src/app.py                 # Streamlit 主入口
├── src/agent.py               # 模拟 Agent 推理
├── src/utils.py               # 数据加载工具
└── tests/                     # 测试脚本（可选）
```

## 页面结构
```
┌─────────────────────────────────────┐
│        恶意 WiFi 安全检测助手        │
│  ┌─────────────────────────────┐    │
│  │    [ 一键扫描周边 WiFi ]     │    │
│  └─────────────────────────────┘    │
│  ┌─────────────────────────────┐    │
│  │  WiFi 列表（扫描结果）       │    │
│  │  ○ Free_Starbucks_WiFi      │    │
│  │  ○ Home_Secure_Net          │    │
│  │  ○ ...                      │    │
│  └─────────────────────────────┘    │
│  ┌─────────────────────────────┐    │
│  │  诊断报告卡片（红/黄/绿）    │    │
│  │  - 风险等级                  │    │
│  │  - 意图分析                  │    │
│  │  - 安全建议                  │    │
│  └─────────────────────────────┘    │
└─────────────────────────────────────┘
```

## 数据流
```
wifi_scenarios.json → utils.load_mock_data() → app.py 展示列表
                                                      ↓
                                           用户选择某个 WiFi
                                                      ↓
                              agent.analyze_wifi_risk(wifi_data)
                                                      ↓
                                         返回 {risk_level, intent_analysis,
                                                security_advice}
                                                      ↓
                                    app.py 根据 risk_level 渲染对应颜色卡片
```

## Agent 风险判定规则
| 条件 | 风险等级 |
|------|----------|
| 加密为 Open 或无加密 + DNS 劫持标记为 true | 高 |
| 加密为 WEP 或 DNS 劫持标记为 true（非 Open） | 中 |
| 加密为 WPA2/WPA3 且 DNS 劫持标记为 false | 低 |
| 未知加密方式 | 中（保守评估） |

## 错误处理
- JSON 文件不存在 → 展示友好错误提示
- JSON 格式错误 → 捕获异常并提示
- 空列表 → 提示"未扫描到 WiFi 信号"
