"""
模拟 AI Agent 推理与诊断逻辑模块。

本模块通过预设规则表来模拟安全专家的 Prompt 意图分析过程，
不涉及任何真实的大模型 API 调用。
"""

from typing import Dict, Any, List


def _build_reasons(encryption: str, dns_hijack: bool, portal_auth: bool, ssid: str) -> List[str]:
    """根据 WiFi 特征构建诊断原因标签列表。"""
    reasons = []

    if encryption == "Open":
        reasons.append("🔓 开放网络")
    elif encryption == "WEP":
        reasons.append("⚠️ WEP弱加密")
    elif encryption in ("WPA2", "WPA3"):
        reasons.append("🔒 " + encryption + "加密")
    else:
        reasons.append("❓ 未知加密")

    if dns_hijack:
        reasons.append("🕵️ DNS劫持风险")

    if portal_auth:
        reasons.append("🔗 Portal认证")

    return reasons


def analyze_wifi_risk(wifi_data: Dict[str, Any]) -> Dict[str, Any]:
    """基于预设规则对单个 WiFi 节点进行风险诊断。

    通过判断加密方式、DNS 劫持风险标志、Portal 认证等特征，
    模拟安全专家的分析思维，输出结构化的诊断报告。

    Args:
        wifi_data: 单个 WiFi 节点的字典数据，需包含 ssid, encryption,
                   dns_hijack_risk, requires_portal_auth 等字段。

    Returns:
        诊断报告字典，包含：
        - risk_level: 风险等级（"高" / "中" / "低"）
        - intent_analysis: 意图分析描述文本
        - security_advice: 安全建议文本
        - diagnosis_reasons: 诊断原因标签列表
    """
    ssid = wifi_data.get("ssid", "未知网络")
    encryption = wifi_data.get("encryption", "未知")
    dns_hijack = wifi_data.get("dns_hijack_risk", False)
    portal_auth = wifi_data.get("requires_portal_auth", False)
    signal = wifi_data.get("signal_strength", 0)

    reasons = _build_reasons(encryption, dns_hijack, portal_auth, ssid)

    # ── 规则 1: 无加密 + DNS 劫持 → 高风险 ──
    if encryption == "Open" and dns_hijack:
        risk_level = "高"
        intent_analysis = (
            f"检测到可疑 WiFi 热点 \"{ssid}\"，该网络未启用任何加密措施（{encryption}），"
            f"且 DNS 解析存在被劫持的风险。信号强度为 {signal}dBm，"
            f"攻击者可能在附近部署了伪基站设备，意图窃取用户的登录凭据、"
            f"浏览记录以及银行卡等敏感信息。建议立即断开连接。"
        )
        security_advice = (
            "【紧急建议】\n\n"
            "1. 请勿连接此 WiFi，也不要通过此网络输入任何账号密码。\n"
            "2. 如已连接，请立即断开并清除手机/电脑中已保存的该网络记录。\n"
            "3. 建议开启移动数据或使用已确认安全的 VPN 进行上网。\n"
            "4. 向场地工作人员确认官方 WiFi 的准确 SSID 名称。"
        )

    # ── 规则 2: WEP 加密 或 Open+DNS劫持组合的次高情况 → 中风险 ──
    elif encryption == "WEP" or (encryption == "Open" and not dns_hijack) or (encryption != "Open" and dns_hijack):
        if encryption == "WEP":
            reason_text = "该网络使用已过时的 WEP 加密协议，此协议可在数分钟内被暴力破解。"
        elif dns_hijack:
            reason_text = f"该网络使用 {encryption} 加密，但 DNS 解析存在被劫持的风险。"
        else:
            reason_text = "该网络为开放式网络，未启用加密，数据传输可能被第三方监听。"

        risk_level = "中"
        intent_analysis = (
            f"WiFi \"{ssid}\" 存在中等安全风险。{reason_text}"
            f"{'同时需要 Portal 认证跳转，认证页面可能被伪造以收集个人信息。' if portal_auth else ''}"
            f"综合判断：该网络可能被攻击者用于中间人攻击（MITM）或信息嗅探。"
        )
        security_advice = (
            "【注意提示】\n\n"
            "1. 尽量避免在此网络下进行敏感操作（网银、登录重要账号等）。\n"
            "2. 如必须使用，请务必开启 VPN 加密通道。\n"
            "3. 注意浏览器地址栏是否出现证书警告，如有请立即停止访问。\n"
            "4. 留意 Portal 认证页面的域名是否为官方域名。"
        )

    # ── 规则 3: WPA2/WPA3 + 无 DNS 劫持 → 低风险 ──
    elif encryption in ("WPA2", "WPA3") and not dns_hijack:
        risk_level = "低"
        intent_analysis = (
            f"WiFi \"{ssid}\" 整体安全状况良好。该网络采用 {encryption} 强加密协议，"
            f"未检测到 DNS 劫持风险，连接安全性较高。"
            f"{'该网络需要通过 Portal 认证登录，属于正常的公共网络管理方式。' if portal_auth else ''}"
        )
        security_advice = (
            "【使用建议】\n\n"
            "1. 该网络安全性较好，可正常使用。\n"
            "2. 建议仍保持操作系统和浏览器的安全更新。\n"
            "3. 在公共场合使用任何 WiFi 时，仍建议对敏感信息操作保持警惕。"
        )

    # ── 规则 4: 未知加密方式 → 中风险（保守评估）──
    else:
        risk_level = "中"
        intent_analysis = (
            f"WiFi \"{ssid}\" 使用了未知的加密方式（{encryption}），"
            f"无法准确评估其安全性。按照安全最佳实践，采取保守策略将其标记为中等风险。"
        )
        security_advice = (
            "【保守建议】\n\n"
            "1. 该网络加密方式未知，建议谨慎连接。\n"
            "2. 如需使用，请开启 VPN 并避免传输敏感信息。\n"
            "3. 如有其他已知安全的网络可选，优先使用备选网络。"
        )

    return {
        "ssid": ssid,
        "risk_level": risk_level,
        "intent_analysis": intent_analysis,
        "security_advice": security_advice,
        "diagnosis_reasons": reasons,
    }
