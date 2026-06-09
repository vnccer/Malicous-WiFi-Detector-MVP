# 恶意 WiFi 检测 MVP — 技术方案

---

## v1.0 技术方案

### 技术栈
- **前端/UI**: Python + Streamlit
- **核心逻辑**: Python 规则引擎（模拟 AI Agent）
- **数据层**: 本地 JSON 文件

### 目录结构
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

### 页面结构
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

### 数据流
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

### Agent 风险判定规则
| 条件 | 风险等级 |
|------|----------|
| 加密为 Open 或无加密 + DNS 劫持标记为 true | 高 |
| 加密为 WEP 或 DNS 劫持标记为 true（非 Open） | 中 |
| 加密为 WPA2/WPA3 且 DNS 劫持标记为 false | 低 |
| 未知加密方式 | 中（保守评估） |

### 错误处理
- JSON 文件不存在 → 展示友好错误提示
- JSON 格式错误 → 捕获异常并提示
- 空列表 → 提示"未扫描到 WiFi 信号"

---

## v2.0 技术方案

### 技术栈
- **前端/UI**: Python + Streamlit（container(border=True) 卡片布局）
- **核心逻辑**: Python 规则引擎（模拟 AI Agent），新增 `diagnosis_reasons` 诊断原因标签
- **数据层**: 本地 JSON 文件（8 个场景，含同名 SSID 伪造场景）
- **反馈持久化**: 本地 JSON 文件 `data/user_feedback.json`

### 目录结构
```
├── data/
│   ├── wifi_scenarios.json     # 模拟 WiFi 场景数据（8 个场景）
│   └── user_feedback.json      # 用户反馈收集（v2.0 新增）
├── docs/
│   ├── spec.md                 # 需求说明（整合版）
│   ├── plan.md                 # 本文件 — 技术方案（整合版）
│   ├── tasks.md                # 任务拆解（整合版）
│   ├── spec_v1.md              # v1.0 需求说明（保留）
│   ├── plan_v1.md              # v1.0 技术方案（保留）
│   ├── tasks_v1.md             # v1.0 任务拆解（保留）
│   ├── spec_v2.md              # v2.0 需求说明（保留）
│   ├── plan_v2.md              # v2.0 技术方案（保留）
│   └── tasks_v2.md             # v2.0 任务拆解（保留）
├── src/
│   ├── app.py                  # Streamlit 主入口（v2.0 重写）
│   ├── agent.py                # 模拟 Agent 推理（新增 diagnosis_reasons）
│   └── utils.py                # 数据加载 + 反馈保存
└── tests/                      # 用户测试反馈文档
```

### 页面结构（v2.0）
```
┌──────────────────────────────────────────────┐
│           恶意 WiFi 安全检测助手              │
│   ┌──────────────────────────────────┐       │
│   │      [ 一键扫描周边 WiFi ]        │       │
│   └──────────────────────────────────┘       │
│                                              │
│   ── WiFi 列表 ───────────────────────       │
│   [📋全部] [🔴高风险] [🟡中风险] [🟢低风险] │ ← v2.0 筛选
│   共 N 个网络（按风险由高到低排列）          │ ← v2.0 排序
│   ⚠️ 存在同名热点，请注意甄别                │ ← v2.0 同名检测
│                                              │
│   ○ 🔴 Free_Starbucks_WiFi  |  ▁▃▅▇ 优秀  | Open  │
│   ○ 🔴 Coffee_Shop_5G ⚠️同名 |  ▁▃▅▇ 优秀  | Open  │
│   ○ 🟡 Airport_Free_WiFi  |  ▁▃▅▇ 优秀  | WEP   │
│   ○ 🟡 CMCC_5G_Free  |  ▁▃▁▁ 较弱  | Open  │
│   ○ 🟢 Coffee_Shop_5G ⚠️同名 |  ▁▃▅▁ 良好  | WPA2  │
│   ○ ...                                      │
│                                              │
│         [ 🔍 开始诊断 ]                      │ ← v2.0 显式触发
│                                              │
│   ┌── 诊断报告卡片 (border) ─────────┐      │
│   │  🔴 风险等级 — 高风险             │      │
│   │  📶 Free_Starbucks_WiFi          │      │
│   │  [🔓开放网络] [🕵️DNS劫持] [🔗Portal] │ ← v2.0 原因标签
│   │  🧠 意图分析                      │      │
│   │  （攻击意图描述文本）              │      │
│   │  🛡️ 安全建议                      │      │
│   │  （分条安全建议）                  │      │
│   └──────────────────────────────────┘      │
│   [ 🚫 加入黑名单 ]                         │ ← v2.0 黑名单
│                                              │
│   ── 黑名单管理 ────────────────────        │
│   🔴 Coffee_Shop_5G | MAC: AA:... | 信道: 48│
│   [🗑 移除]                                  │
│                                              │
│   ── 💬 用户反馈 ────────────────────       │ ← v2.0 反馈
│   [文本输入框]  [📤 提交反馈]                │
│                                              │
│   ═══════════════════════════════════        │
│   侧边栏：关于 / 风险等级说明                 │
└──────────────────────────────────────────────┘
```

### 数据流（v2.0）
```
wifi_scenarios.json → utils.load_mock_data()
                             ↓
                     app.py: 快速风险排序 + 同名检测
                             ↓
                     app.py: 展示列表（含风险图标、信号图标）
                             ↓
                    用户选择 WiFi → 点击「开始诊断」
                             ↓
             agent.analyze_wifi_risk(wifi_data)
                             ↓
   返回 {risk_level, intent_analysis, security_advice, diagnosis_reasons}
                             ↓
        app.py: render_risk_card() → container(border=True) 卡片
                             ↓
        用户可选：加入黑名单 / 提交反馈 / 切换筛选
```

### Agent 风险判定规则（v2.0）
| 条件 | 风险等级 | 诊断原因标签 |
|------|----------|-------------|
| 加密为 Open + DNS 劫持 | **高** | 🔓开放网络 🕵️DNS劫持风险 (+ 🔗Portal认证) |
| 加密为 WEP | 中 | ⚠️WEP弱加密 |
| 加密为 Open 但无 DNS 劫持 | 中 | 🔓开放网络 |
| 加密非 Open 但 DNS 劫持 | 中 | 🔒XX加密 🕵️DNS劫持风险 |
| 加密为 WPA2/WPA3 且无 DNS 劫持 | 低 | 🔒XX加密 (+ 🔗Portal认证) |
| 未知加密方式 | 中（保守） | ❓未知加密 |

### 关键设计决策

#### WiFi 唯一标识
- **v1.0**：使用 SSID 作为 key → 同名 SSID 互相覆盖
- **v2.0**：使用 MAC 地址作为 key，支持同名热点并存，界面标注 ⚠️同名

#### 信号强度显示
- **v1.0**：使用 `abs(signal)` 显示正值
- **v2.0**：显示真实负值 dBm，按区间映射信号图标：
  - ≥ -50dBm → ▁▃▅▇ 优秀
  - -70 ~ -50dBm → ▁▃▅▁ 良好
  - < -70dBm → ▁▃▁▁ 较弱

#### 风险卡片渲染
- **v1.0**：`with st.error/warning/success():` 上下文管理器 → 仅渲染最后一个子元素（**已知 bug**）
- **v2.0**：`with st.container(border=True):` → 所有子元素正常渲染

#### 诊断触发
- **v1.0**：选择 radio 即自动触发诊断 → 用户不知道报告是否更新
- **v2.0**：选择 + 点击「开始诊断」按钮 → 交互意图明确

### 错误处理
- JSON 文件不存在 → 展示友好错误提示
- JSON 格式错误 → 捕获异常并提示
- 空列表 → 提示"未扫描到 WiFi 信号"
- 筛选后无结果 → 提示"当前没有标记为「XX风险」的 WiFi 网络"
- 反馈保存失败 → 提示用户稍后重试
