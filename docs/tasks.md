# 恶意 WiFi 检测 MVP — 开发任务拆解

---

## v1.0 任务列表

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

---

## v2.0 任务拆解

### v1.0 任务回顾（全部完成）
v1.0 共 7 个任务，建立了项目骨架：目录结构、Mock 数据（4 场景）、三份文档、utils/agent/app 三大模块。

### v2.0 迭代背景
基于用户测试反馈（`tests/43027used.md`、`tests/测试建议v1.docx`），识别出以下核心问题：
1. 同名 SSID 覆盖导致关键风险场景被抹掉
2. 风险卡片视觉感不强，意图分析不够直观
3. 信号显示使用 abs() 导致信号值失真
4. 缺少风险排序、筛选、黑名单、用户反馈等功能
5. 诊断触发不明确，用户不知道报告是否更新

---

### 1. 扩展测试数据集 (15 min)
- [x] 在 `data/wifi_scenarios.json` 中新增 4 个场景（共计 8 个）
- [x] 新增伪造同名 SSID 场景（`Coffee_Shop_5G` 正规版 vs 恶意版）
- [x] 新增酒店、移动运营商、图书馆等多样化场景
- [x] 确保所有节点包含 `mac_address`、`channel` 字段

### 2. 增强 Agent 诊断输出 (10 min)
- [x] `src/agent.py` 新增 `_build_reasons()` — 根据特征生成诊断原因标签列表
- [x] `analyze_wifi_risk()` 返回值新增 `diagnosis_reasons` 字段
- [x] 标签分类：加密方式、DNS 风险、Portal 认证、未知加密
- [x] 修正信号值引用，去掉 abs()

### 3. 修复核心渲染 Bug (15 min)
- [x] 发现 `st.error/warning/success` 上下文管理器仅渲染最后子元素的 bug
- [x] 改用 `st.container(border=True)` 替代，确保风险卡片所有内容正常渲染
- [x] 风险卡片重组：标题 → SSID → 原因标签 → 意图分析 → 安全建议

### 4. WiFi 列表增强 (20 min)
- [x] 用 MAC 地址替代 SSID 作为 WiFi 唯一标识，修复同名覆盖问题
- [x] 新增 `quick_risk()` 快速风险评估函数（用于排序和筛选）
- [x] 新增 `get_signal_icon()` — 信号强度分级图标（优秀/良好/较弱）
- [x] 列表按风险从高到低排序
- [x] 每个 WiFi 显示 🔴🟡🟢 风险图标 + 信号图标 + 加密方式
- [x] 同名 SSID 检测与 ⚠️ 警告显示
- [x] 新增 全部/高风险/中风险/低风险 四个筛选按钮

### 5. 显式诊断触发 (10 min)
- [x] WiFi 选择与诊断报告解耦：选择不自动触发诊断
- [x] 新增「🔍 开始诊断」按钮，点击后更新报告
- [x] 筛选切换时重置已选 WiFi 和报告状态

### 6. 黑名单功能 (10 min)
- [x] 高风险诊断报告下显示「加入黑名单」按钮
- [x] 黑名单存储在 `st.session_state.blacklist`
- [x] 黑名单管理区展示已标记 WiFi 的详细信息
- [x] 支持从黑名单移除

### 7. 用户反馈收集 (10 min)
- [x] `src/utils.py` 新增 `save_feedback()` — 保存反馈到 `data/user_feedback.json`
- [x] 页面底部增加可展开的反馈区（`st.expander`）
- [x] 文本输入框 + 提交按钮
- [x] 提交后显示成功提示并清空输入框

### 8. 侧边栏改进 (5 min)
- [x] 新增「风险等级说明」区域，解释红/黄/绿含义
- [x] 保留原有"关于本工具"说明

### 9. 集成测试与验证 (15 min)
- [x] 启动 Streamlit 验证完整流程
- [x] Playwright 自动化验证 17 个检查点全部通过
- [x] 验证同名热点检测
- [x] 验证筛选 + 排序
- [x] 验证诊断报告完整性（原因标签、意图分析、安全建议）
- [x] 验证黑名单增删
- [x] 验证反馈提交与持久化

---

### v2.0 任务汇总

| 任务 | 耗时 | 涉及文件 |
|------|------|---------|
| 1. 扩展测试数据集 | 15 min | `data/wifi_scenarios.json` |
| 2. 增强 Agent 诊断 | 10 min | `src/agent.py` |
| 3. 修复渲染 Bug | 15 min | `src/app.py` |
| 4. WiFi 列表增强 | 20 min | `src/app.py` |
| 5. 显式诊断触发 | 10 min | `src/app.py` |
| 6. 黑名单功能 | 10 min | `src/app.py` |
| 7. 用户反馈收集 | 10 min | `src/utils.py`, `src/app.py` |
| 8. 侧边栏改进 | 5 min | `src/app.py` |
| 9. 集成测试验证 | 15 min | 全量验证 |
| **合计** | **110 min** | |

---

### v1.0 → v2.0 关键变更对照

| 维度 | v1.0 | v2.0 |
|------|------|------|
| 测试场景 | 4 个 | 8 个（含同名伪造） |
| WiFi 标识 | SSID | MAC 地址 |
| 信号显示 | abs() 正值 | 真实负值 + 图标 |
| 风险卡片 | st.error 上下文（有 bug） | container(border=True) |
| 诊断触发 | 自动（选择即触发） | 显式按钮 |
| 诊断输出 | 3 字段 | 4 字段（+ diagnosis_reasons） |
| 列表排序 | 无序 | 风险高→低 |
| 风险筛选 | 无 | 全部/高/中/低 |
| 黑名单 | 无 | 有 |
| 用户反馈 | 无 | 有 |
| 同名检测 | 无 | 有 |
