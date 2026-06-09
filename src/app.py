"""
恶意 WiFi 安全检测助手 — Streamlit 主程序入口。
"""

from collections import Counter

import streamlit as st

from utils import load_mock_data, save_feedback
from agent import analyze_wifi_risk


# ── 页面基础配置 ──
st.set_page_config(
    page_title="恶意 WiFi 安全检测助手",
    page_icon="🛡️",
    layout="centered",
)

# ── 常量 ──
RISK_ORDER = {"高": 0, "中": 1, "低": 2}
RISK_EMOJI = {"高": "🔴", "中": "🟡", "低": "🟢"}
RISK_COLOR = {"高": "#ff4b4b", "中": "#ffaa00", "低": "#00c853"}


# ═══════════════════════════════════════════════════════════════
# 辅助函数
# ═══════════════════════════════════════════════════════════════

def get_wifi_uid(node: dict) -> str:
    """获取 WiFi 节点的唯一标识（优先使用 MAC 地址）。"""
    mac = node.get("mac_address", "")
    if mac:
        return mac
    ch = node.get("channel", 0)
    return f"{node.get('ssid', 'unknown')}_{ch}"


def quick_risk(node: dict) -> str:
    """快速评估风险等级，用于排序和筛选（无需完整诊断）。"""
    enc = node.get("encryption", "")
    dns = node.get("dns_hijack_risk", False)
    if enc == "Open" and dns:
        return "高"
    elif enc == "WEP" or enc == "Open" or dns:
        return "中"
    else:
        return "低"


def get_signal_icon(strength: int) -> tuple:
    """根据 dBm 信号值返回图标和文字等级。"""
    if strength >= -50:
        return "▁▃▅▇", "优秀"
    elif strength >= -70:
        return "▁▃▅▁", "良好"
    else:
        return "▁▃▁▁", "较弱"


def render_diagnosis_reasons(reasons: list, color: str):
    """渲染诊断原因标签行。"""
    if not reasons:
        return
    tags_html = "".join(
        f"<span style='"
        f"background:{color}18;"
        f"border:1px solid {color}60;"
        f"border-radius:14px;"
        f"padding:3px 12px;"
        f"margin-right:6px;"
        f"font-size:0.85rem;"
        f"white-space:nowrap;"
        f"'>{r}</span>"
        for r in reasons
    )
    st.markdown(
        f"<div style='margin:8px 0 14px 0;line-height:2.2;'>{tags_html}</div>",
        unsafe_allow_html=True,
    )


def render_risk_card(report: dict):
    """增强版风险卡片：风险等级 + 诊断原因标签 + 意图分析 + 安全建议。"""
    risk = report.get("risk_level", "中")
    ssid = report.get("ssid", "未知")
    analysis = report.get("intent_analysis", "")
    advice = report.get("security_advice", "")
    reasons = report.get("diagnosis_reasons", [])
    emoji = RISK_EMOJI.get(risk, "⚪")
    color = RISK_COLOR.get(risk, "#888")

    # 使用 container(border=True) 提供卡片感，内部用彩色标题区分风险等级
    with st.container(border=True):
        # 风险等级标题（带颜色）
        st.markdown(f"### {emoji} 风险等级 — {risk}风险")
        st.caption(f"📶 **{ssid}**")

        # 诊断原因标签
        render_diagnosis_reasons(reasons, color)

        # 意图分析
        st.markdown("**🧠 意图分析**")
        st.write(analysis)

        # 安全建议
        st.markdown("**🛡️ 安全建议**")
        st.markdown(advice)


# ═══════════════════════════════════════════════════════════════
# 主程序
# ═══════════════════════════════════════════════════════════════

def main():
    # ── 标题区 ──
    st.title("🛡️ 恶意 WiFi 安全检测助手")
    st.caption("基于 AI Agent 的 WiFi 网络风险诊断工具（模拟数据演示）")
    st.divider()

    # ── 初始化会话状态 ──
    defaults = {
        "wifi_list": [],
        "selected_wifi_id": None,
        "current_report": None,
        "blacklist": [],
        "filter_level": "全部",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

    # ── 一键扫描按钮 ──
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        scan_clicked = st.button(
            "📡 一键扫描周边 WiFi",
            type="primary",
            use_container_width=True,
        )

    if scan_clicked:
        with st.spinner("正在扫描周边 WiFi 信号，请稍候..."):
            try:
                st.session_state.wifi_list = load_mock_data()
                st.session_state.selected_wifi_id = None
                st.session_state.current_report = None
                st.toast(f"✅ 扫描完成！发现 {len(st.session_state.wifi_list)} 个 WiFi 信号", icon="✅")
            except FileNotFoundError as e:
                st.error(f"❌ 数据文件未找到\n\n{e}")
                st.session_state.wifi_list = []
            except ValueError as e:
                st.warning(f"⚠️ 数据异常\n\n{e}")
                st.session_state.wifi_list = []
            except Exception as e:
                st.error(f"❌ 未知错误: {e}")
                st.session_state.wifi_list = []

    # ── WiFi 列表展示区 ──
    if st.session_state.wifi_list:
        st.divider()
        st.subheader("📋 已发现的 WiFi 网络")

        wifi_list = st.session_state.wifi_list

        # 构建完整映射（包含所有 WiFi，用于黑名单展示）
        full_map = {get_wifi_uid(n): n for n in wifi_list}

        # 检测同名 SSID
        ssid_counts = Counter(n["ssid"] for n in wifi_list)
        dup_ssids = {s for s, c in ssid_counts.items() if c > 1}

        # ── 风险筛选按钮 ──
        filter_cols = st.columns(4)
        filter_opts = [
            ("全部", "📋"),
            ("高", "🔴"),
            ("中", "🟡"),
            ("低", "🟢"),
        ]
        for i, (level, icon) in enumerate(filter_opts):
            with filter_cols[i]:
                label = f"{icon} {level}风险" if level != "全部" else f"{icon} 全部"
                is_active = st.session_state.filter_level == level
                if st.button(
                    label,
                    key=f"flt_{level}",
                    type="primary" if is_active else "secondary",
                    use_container_width=True,
                ):
                    st.session_state.filter_level = level
                    st.session_state.selected_wifi_id = None
                    st.session_state.current_report = None
                    st.rerun()

        # ── 排序：按风险从高到低 ──
        sorted_all = sorted(wifi_list, key=lambda n: RISK_ORDER.get(quick_risk(n), 99))

        # ── 按选中等级筛选 ──
        current_filter = st.session_state.filter_level
        if current_filter != "全部":
            filtered = [n for n in sorted_all if quick_risk(n) == current_filter]
        else:
            filtered = sorted_all

        filtered_map = {get_wifi_uid(n): n for n in filtered}
        uid_list = list(filtered_map.keys())

        if not uid_list:
            st.info(f"当前没有标记为「{current_filter}风险」的 WiFi 网络。")
        else:
            st.caption(
                f"共 {len(uid_list)} 个网络（按风险由高到低排列）"
                + ("  |  ⚠️ 存在同名热点，请注意甄别" if dup_ssids else "")
            )

            # ── WiFi 选择列表 ──
            def format_label(uid: str) -> str:
                node = filtered_map[uid]
                ssid = node["ssid"]
                risk = quick_risk(node)
                sig_icon, sig_label = get_signal_icon(node.get("signal_strength", -100))
                enc = node.get("encryption", "?")
                dup_mark = " ⚠️同名" if ssid in dup_ssids else ""
                return f"{RISK_EMOJI[risk]} {ssid}{dup_mark}  |  {sig_icon} {sig_label}  |  {enc}"

            selected_id = st.radio(
                "请选择要诊断的 WiFi 网络：",
                options=uid_list,
                format_func=format_label,
                key="wifi_selector",
            )

            # ── 开始诊断按钮 ──
            st.markdown("")
            dcol1, dcol2, dcol3 = st.columns([1, 1, 1])
            with dcol2:
                diag_clicked = st.button(
                    "🔍 开始诊断",
                    type="primary",
                    use_container_width=True,
                )

            if diag_clicked and selected_id:
                st.session_state.selected_wifi_id = selected_id
                node = filtered_map[selected_id]
                st.session_state.current_report = analyze_wifi_risk(node)

            # ── 诊断报告区 ──
            if st.session_state.current_report and st.session_state.selected_wifi_id:
                st.divider()
                st.subheader("🔍 诊断报告")
                render_risk_card(st.session_state.current_report)

                # ── 黑名单操作 ──
                report_risk = st.session_state.current_report.get("risk_level", "")
                current_id = st.session_state.selected_wifi_id

                if report_risk == "高":
                    st.markdown("")
                    if current_id not in st.session_state.blacklist:
                        if st.button("🚫 将该 WiFi 加入黑名单", type="secondary"):
                            st.session_state.blacklist.append(current_id)
                            st.toast("已加入黑名单，后续扫描将重点标记此热点", icon="🚫")
                            st.rerun()
                    else:
                        if st.button("🚫 已加入黑名单 — 点击移除", type="secondary"):
                            st.session_state.blacklist.remove(current_id)
                            st.toast("已从黑名单中移除", icon="✅")
                            st.rerun()

        # ── 黑名单管理区 ──
        if st.session_state.blacklist:
            st.divider()
            st.subheader("🚫 黑名单管理")
            for wid in list(st.session_state.blacklist):
                node = full_map.get(wid)
                if node is None:
                    # 节点可能已被移除，清理
                    st.session_state.blacklist.remove(wid)
                    continue
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.markdown(
                        f"🔴 **{node['ssid']}**  |  "
                        f"MAC: `{node.get('mac_address', '?')}`  |  "
                        f"信道: {node.get('channel', '?')}  |  "
                        f"加密: {node.get('encryption', '?')}"
                    )
                with c2:
                    if st.button("🗑 移除", key=f"rmbl_{wid}", use_container_width=True):
                        st.session_state.blacklist.remove(wid)
                        st.rerun()

    elif scan_clicked:
        st.info("未发现任何 WiFi 信号，请确认扫描环境。")

    # 通过递增计数器改变 widget key，实现提交后清空输入框
    if "feedback_key_counter" not in st.session_state:
        st.session_state.feedback_key_counter = 0

    # ── 用户反馈区 ──
    st.divider()
    with st.expander("💬 用户反馈"):
        st.caption("如果您有任何改进建议或使用体验反馈，请在下方留言。")
        feedback_key = f"feedback_input_{st.session_state.feedback_key_counter}"
        feedback_text = st.text_area(
            "反馈内容",
            placeholder="请输入您的建议或遇到的问题...",
            label_visibility="collapsed",
            key=feedback_key,
        )
        fb_col1, fb_col2, _ = st.columns([1, 1, 2])
        with fb_col1:
            if st.button("📤 提交反馈", use_container_width=True):
                if feedback_text.strip():
                    ok = save_feedback(feedback_text.strip())
                    if ok:
                        st.success("感谢您的反馈！我们会认真考虑您的建议。")
                        st.session_state.feedback_key_counter += 1
                        st.rerun()
                    else:
                        st.error("反馈保存失败，请稍后重试。")
                else:
                    st.warning("请先输入反馈内容再提交。")

    # ── 侧边栏说明 ──
    with st.sidebar:
        st.markdown("## ℹ️ 关于本工具")
        st.markdown(
            """
            本项目是一个 **MVP 演示系统**，用于展示
            基于 Agent 的 WiFi 安全检测流程。

            **重要说明：**
            - 所有数据均为本地模拟数据
            - 不涉及真实网络扫描
            - Agent 诊断基于预设规则引擎
            - 仅供学习与课程演示用途
            """
        )
        st.divider()
        st.markdown("### 🚦 风险等级说明")
        st.markdown(
            """
            - 🔴 **高风险**：开放网络 + DNS 劫持
            - 🟡 **中风险**：弱加密 / 可疑特征
            - 🟢 **低风险**：WPA2/WPA3 强加密
            """
        )
        st.divider()
        st.caption("恶意 WiFi 检测 MVP  |  数据分析课程项目")


if __name__ == "__main__":
    main()
