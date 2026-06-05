"""
恶意 WiFi 安全检测助手 — Streamlit 主程序入口。
"""

import streamlit as st
from utils import load_mock_data
from agent import analyze_wifi_risk


# ── 页面基础配置 ──
st.set_page_config(
    page_title="恶意 WiFi 安全检测助手",
    page_icon="🛡️",
    layout="centered",
)


def render_risk_card(report: dict):
    """根据风险等级渲染对应颜色的诊断卡片。"""
    risk = report.get("risk_level", "中")
    ssid = report.get("ssid", "未知")
    analysis = report.get("intent_analysis", "")
    advice = report.get("security_advice", "")

    if risk == "高":
        container = st.error
        emoji = "🔴"
    elif risk == "中":
        container = st.warning
        emoji = "🟡"
    else:
        container = st.success
        emoji = "🟢"

    with container(f"{emoji} 风险等级 — {risk}风险"):
        st.markdown(f"### 📶 {ssid}")
        st.markdown("**🧠 意图分析**")
        st.write(analysis)
        st.markdown("**🛡️ 安全建议**")
        st.markdown(advice)


def main():
    # ── 标题区 ──
    st.title("🛡️ 恶意 WiFi 安全检测助手")
    st.caption("基于 AI Agent 的 WiFi 网络风险诊断工具（模拟数据演示）")
    st.divider()

    # ── 初始化会话状态 ──
    if "wifi_list" not in st.session_state:
        st.session_state.wifi_list = []
    if "selected_ssid" not in st.session_state:
        st.session_state.selected_ssid = None

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
                st.session_state.selected_ssid = None
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

        wifi_map = {node["ssid"]: node for node in st.session_state.wifi_list}
        ssid_options = list(wifi_map.keys())

        selected = st.radio(
            "请选择要诊断的 WiFi 网络：",
            options=ssid_options,
            format_func=lambda x: f"📶 {x}  |  加密: {wifi_map[x]['encryption']}  |  信号: {abs(wifi_map[x]['signal_strength'])}dBm",
            key="wifi_selector",
        )

        if selected and selected != st.session_state.selected_ssid:
            st.session_state.selected_ssid = selected

        # ── 诊断报告区 ──
        if st.session_state.selected_ssid:
            st.divider()
            st.subheader("🔍 诊断报告")
            wifi_node = wifi_map[st.session_state.selected_ssid]
            report = analyze_wifi_risk(wifi_node)
            render_risk_card(report)

    elif scan_clicked:
        st.info("未发现任何 WiFi 信号，请确认扫描环境。")

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
        st.caption("恶意 WiFi 检测 MVP  |  数据分析课程项目")


if __name__ == "__main__":
    main()
