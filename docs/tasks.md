# 恶意 WiFi 检测 MVP — 开发任务拆解

## 任务列表

### 1. 创建项目目录结构 (5 min)
- [x] 创建 `data/`, `docs/`, `src/`, `tests/` 目录

### 2. 生成 Mock 数据 (10 min)
- [x] 创建 `data/wifi_scenarios.json`
- [x] 包含 4 个场景：1 个低风险 / 1 个中风险 / 1 个高风险伪造热点 / 1 个高风险机场 WiFi

### 3. 编写文档 (10 min)
- [x] `docs/spec.md` — 需求规格说明
- [x] `docs/plan.md` — 技术方案与架构
- [x] `docs/tasks.md` — 本文件

### 4. 开发 utils.py (10 min)
- [x] `load_mock_data()` — 加载 JSON 并处理异常
- [x] 文件不存在、格式错误、空数据的错误处理

### 5. 开发 agent.py (15 min)
- [x] `analyze_wifi_risk(wifi_data)` — 基于规则的风险诊断
- [x] 返回 `{risk_level, intent_analysis, security_advice}` 字典

### 6. 开发 app.py (20 min)
- [x] "一键扫描周边 WiFi" 按钮
- [x] WiFi 列表展示与选择
- [x] 调用 agent 获取诊断报告
- [x] 红/黄/绿灯卡片视觉展示

### 7. 集成测试与验证 (10 min)
- [x] 启动 Streamlit 验证完整流程
- [x] 验证高风险/中风险/低风险三个路径
- [x] 验证 JSON 缺失的错误处理
