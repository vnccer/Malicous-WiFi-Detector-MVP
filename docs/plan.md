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

---

## v3.0 技术方案

### 技术栈（同 v2.0）
- **前端/UI**: Python + Streamlit（container(border=True) 卡片布局）
- **核心逻辑**: Python 规则引擎（模拟 AI Agent）
- **数据层**: 本地 JSON 文件 + `data/blacklist_notes.json`（v3.0 新增）

### 目录结构（v3.0 新增）
```
data/
├── wifi_scenarios.json
├── user_feedback.json
└── blacklist_notes.json        # v3.0 新增：黑名单备注持久化
```

### 页面结构（v3.0 新增区域）
```
  ── WiFi 列表 ───────────────────────
  [📋全部(8)] [🔴高风险(2)] [🟡中风险(2)] [🟢低风险(4)]   ← v3.0 计数

  ○ 🔴 Free_Starbucks_WiFi  |  ...  |  Open  🚫已拉黑 🏷「可疑热点」 ← v3.0 备注标签

  ── 诊断报告 ───────────────────────
  ┌── 风险卡片 ────────────────────┐
  │  ...                          │
  └───────────────────────────────┘
  [ 备注: ______ ]  [ 🚫 加入黑名单 ]    ← v3.0 备注输入

  ── WiFi 对比分析 ────────────────────   ← v3.0 全新区域
  [ 选择 WiFi A ▼ ]  [ 选择 WiFi B ▼ ]
        [ ⚖️ 开始对比 ]

  ┌── 对比结果 ────────────────────┐
  │  📶 A: 85分 +15  ⚡VS⚡  📶 B: 70分  │
  │  📊 五维度详细对比              │
  │  高风险 ✅  |  风险等级  |  中风险    │
  │  Open      |  加密方式  |  WPA2 ✅  │
  │  ...                          │
  │  🏆 建议连接：WiFi B           │
  └───────────────────────────────┘
```

### 数据流（v3.0 新增）
```
用户添加备注 → blacklist_notes[uid] = note
                     ↓
        save_blacklist_notes() → data/blacklist_notes.json
                     ↓
        下次启动: load_blacklist_notes() → st.session_state

对比流程:
  选择 WiFi A + WiFi B → 点击「开始对比」
                     ↓
        agent.compare_wifi(node_a, node_b)
                     ↓
        返回 {score_a, score_b, dimensions[], recommendation, summary}
                     ↓
        app.py 渲染双栏评分卡片 + 五维度对比表 + 综合建议
```

### WiFi 对比评分规则（v3.0 新增）
综合评分满分 100 分，分四个维度：
| 维度 | 满分 | 评分规则 |
|------|------|---------|
| 加密方式 | 30 | WPA3: 30, WPA2: 22, WEP: 8, Open: 0, 未知: 5 |
| DNS 劫持风险 | 30 | 无风险: 30, 有风险: 0 |
| 信号强度 | 25 | ≥ -50dBm: 25, -70~-50: 15, < -70: 5 |
| Portal 认证 | 15 | 无需认证: 15, 需要认证: 0 |

### 关键设计决策（v3.0）

#### 黑名单备注存储
- 使用独立 JSON 文件 `data/blacklist_notes.json`
- 数据结构：`{wifi_uid: note_text}`
- 备注限制 2-5 字符，用于 icon 展示
- 与 `st.session_state.blacklist` 解耦，但同步增删

#### WiFi 对比选择器
- 使用两个 `st.selectbox` 而非 `st.multiselect`
- 第二个选择框自动排除第一个已选 WiFi
- 对比基于完整 WiFi 列表（不受当前筛选影响）

#### 对比结果渲染
- 综合评分使用 `st.metric` 组件，差值三角形指示领先方
- 五维度对比使用自定义 HTML，优胜方绿色高亮 + ✅ 标记
- 综合建议使用 `st.container(border=True)` 卡片

---

## v4.0 技术方案

### 迭代背景
v3.0 上线后发现三个交互缺陷：
1. 未扫描时对比区域完全隐藏，用户感知不到该功能存在
2. `st.session_state.blacklist` 仅存内存，页面刷新后丢失，但备注文件仍保留，导致数据不一致
3. 黑名单按钮仅高风险可见，用户无法拉黑中/低风险的伪造热点

### 变更点

#### 1. 对比区域始终可见
```python
# 旧: if st.session_state.wifi_list and len(...) >= 2: <全部内容>
# 新: 标题始终渲染，if/else 分支控制提示文案 vs 交互组件
if not st.session_state.wifi_list or len(st.session_state.wifi_list) < 2:
    st.info("请先扫描周边 WiFi，扫描完成后可在此选择两个网络进行并排对比分析。")
else:
    st.caption("选择两个 WiFi 进行并排对比...")
    # ... 交互组件
```

#### 2. 黑名单持久化
- **方案**：`blacklist` 列表与 `blacklist_notes` 字典的 keys 保持同步
- 启动时：加载 `blacklist_notes.json` → 用 `list(notes.keys())` 恢复 blacklist
- 增删时：两者同步操作 + 写文件
- 无需新增独立文件，复用现有 `blacklist_notes.json`

```python
if key == "blacklist_notes":
    notes = load_blacklist_notes()
    st.session_state["blacklist_notes"] = notes
    st.session_state["blacklist"] = list(notes.keys())
```

#### 3. 全风险等级可拉黑
- 移除 `if report_risk == "高":` 守卫条件
- 黑名单按钮对所有诊断完成的 WiFi 可见
- 黑名单管理区：用 `quick_risk(node)` + `RISK_EMOJI` 替代硬编码 🔴

### 关键设计决策（v4.0）

#### 黑名单数据一致性
- `blacklist` 与 `blacklist_notes` 不再是解耦关系，而是派生关系
- `blacklist = list(blacklist_notes.keys())` 始终为真
- 优势：单一数据源（文件），消除不一致状态

#### 对比区域 UX
- 标题和分隔线始终渲染 → 用户始终知道此功能存在
- 未扫描时显示引导文案 → 降低学习成本
- 扫描后自动切换到交互模式 → 用户无感知切换
