"""
模拟 AI Agent 推理与诊断逻辑模块。

本模块通过预设规则表来模拟安全专家的 Prompt 意图分析过程，
不涉及任何真实的大模型 API 调用。
"""

from typing import Dict, Any, List, Tuple


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


def _encryption_rank(enc: str) -> int:
    """加密方式优劣排名（数值越大越安全）。"""
    ranking = {"WPA3": 4, "WPA2": 3, "WEP": 1, "Open": 0}
    return ranking.get(enc, 0)


def _signal_rank(strength: int) -> int:
    """信号强度优劣排名（数值越大越好）。"""
    if strength >= -50:
        return 3
    elif strength >= -70:
        return 2
    else:
        return 1


def _calc_score(node: Dict[str, Any]) -> int:
    """计算 WiFi 综合安全评分（满分 100）。"""
    score = 0
    enc = node.get("encryption", "")
    dns = node.get("dns_hijack_risk", False)
    signal = node.get("signal_strength", -100)
    portal = node.get("requires_portal_auth", False)

    # 加密方式：满分 30
    enc_scores = {"WPA3": 30, "WPA2": 22, "WEP": 8, "Open": 0}
    score += enc_scores.get(enc, 5)

    # DNS 劫持风险：满分 30
    if not dns:
        score += 30

    # 信号强度：满分 25
    if signal >= -50:
        score += 25
    elif signal >= -70:
        score += 15
    else:
        score += 5

    # Portal 认证：满分 15（无 Portal 更安全）
    if not portal:
        score += 15

    return score


def compare_wifi(wifi_a: Dict[str, Any], wifi_b: Dict[str, Any]) -> Dict[str, Any]:
    """对比两个 WiFi 网络，给出连接建议。

    从风险等级、加密方式、信号强度、DNS 劫持风险、Portal 认证
    五个维度进行综合对比，生成并排分析报告。

    Args:
        wifi_a: 第一个 WiFi 节点字典。
        wifi_b: 第二个 WiFi 节点字典。

    Returns:
        对比报告字典，包含：
        - score_a / score_b: 综合评分
        - dimensions: 各维度对比列表
        - recommendation: 建议连接方（"A" / "B" / "持平"）
        - summary: 综合建议文本
    """
    risk_a = analyze_wifi_risk(wifi_a)["risk_level"]
    risk_b = analyze_wifi_risk(wifi_b)["risk_level"]

    RISK_ORDER = {"高": 0, "中": 1, "低": 2}

    dimensions: List[Dict[str, Any]] = []

    # ── 维度 1: 风险等级对比 ──
    dim_risk = {
        "name": "风险等级",
        "icon": "⚠️",
        "value_a": f"{risk_a}风险",
        "value_b": f"{risk_b}风险",
    }
    if RISK_ORDER[risk_a] > RISK_ORDER[risk_b]:
        dim_risk["winner"] = "A"
        dim_risk["detail"] = f"{wifi_a['ssid']} 风险更低，更安全"
    elif RISK_ORDER[risk_a] < RISK_ORDER[risk_b]:
        dim_risk["winner"] = "B"
        dim_risk["detail"] = f"{wifi_b['ssid']} 风险更低，更安全"
    else:
        dim_risk["winner"] = "持平"
        dim_risk["detail"] = "两者风险等级相同"
    dimensions.append(dim_risk)

    # ── 维度 2: 加密方式对比 ──
    enc_a = wifi_a.get("encryption", "未知")
    enc_b = wifi_b.get("encryption", "未知")
    dim_enc = {
        "name": "加密方式",
        "icon": "🔐",
        "value_a": enc_a,
        "value_b": enc_b,
    }
    rank_a = _encryption_rank(enc_a)
    rank_b = _encryption_rank(enc_b)
    if rank_a > rank_b:
        dim_enc["winner"] = "A"
        dim_enc["detail"] = f"{enc_a} 安全性优于 {enc_b}"
    elif rank_a < rank_b:
        dim_enc["winner"] = "B"
        dim_enc["detail"] = f"{enc_b} 安全性优于 {enc_a}"
    else:
        dim_enc["winner"] = "持平"
        dim_enc["detail"] = "两者加密方式相同"
    dimensions.append(dim_enc)

    # ── 维度 3: 信号强度对比 ──
    sig_a = wifi_a.get("signal_strength", -100)
    sig_b = wifi_b.get("signal_strength", -100)
    dim_sig = {
        "name": "信号强度",
        "icon": "📶",
        "value_a": f"{sig_a} dBm",
        "value_b": f"{sig_b} dBm",
    }
    sr_a = _signal_rank(sig_a)
    sr_b = _signal_rank(sig_b)
    if sr_a > sr_b:
        dim_sig["winner"] = "A"
        dim_sig["detail"] = f"{wifi_a['ssid']} 信号更强（{sig_a} vs {sig_b} dBm）"
    elif sr_a < sr_b:
        dim_sig["winner"] = "B"
        dim_sig["detail"] = f"{wifi_b['ssid']} 信号更强（{sig_b} vs {sig_a} dBm）"
    else:
        dim_sig["winner"] = "持平"
        dim_sig["detail"] = "两者信号强度相当"
    dimensions.append(dim_sig)

    # ── 维度 4: DNS 劫持风险对比 ──
    dns_a = wifi_a.get("dns_hijack_risk", False)
    dns_b = wifi_b.get("dns_hijack_risk", False)
    dim_dns = {
        "name": "DNS 劫持",
        "icon": "🕵️",
        "value_a": "⚠️ 有风险" if dns_a else "✅ 安全",
        "value_b": "⚠️ 有风险" if dns_b else "✅ 安全",
    }
    if not dns_a and dns_b:
        dim_dns["winner"] = "A"
        dim_dns["detail"] = f"{wifi_a['ssid']} 无 DNS 劫持风险"
    elif dns_a and not dns_b:
        dim_dns["winner"] = "B"
        dim_dns["detail"] = f"{wifi_b['ssid']} 无 DNS 劫持风险"
    elif not dns_a and not dns_b:
        dim_dns["winner"] = "持平"
        dim_dns["detail"] = "两者均无 DNS 劫持风险"
    else:
        dim_dns["winner"] = "持平"
        dim_dns["detail"] = "两者均存在 DNS 劫持风险，都不建议连接"
    dimensions.append(dim_dns)

    # ── 维度 5: Portal 认证对比 ──
    portal_a = wifi_a.get("requires_portal_auth", False)
    portal_b = wifi_b.get("requires_portal_auth", False)
    dim_portal = {
        "name": "Portal 认证",
        "icon": "🔗",
        "value_a": "需要认证" if portal_a else "无需认证",
        "value_b": "需要认证" if portal_b else "无需认证",
    }
    if not portal_a and portal_b:
        dim_portal["winner"] = "A"
        dim_portal["detail"] = f"{wifi_a['ssid']} 无需 Portal 认证，减少钓鱼风险"
    elif portal_a and not portal_b:
        dim_portal["winner"] = "B"
        dim_portal["detail"] = f"{wifi_b['ssid']} 无需 Portal 认证，减少钓鱼风险"
    elif not portal_a and not portal_b:
        dim_portal["winner"] = "持平"
        dim_portal["detail"] = "两者均无需 Portal 认证"
    else:
        dim_portal["winner"] = "持平"
        dim_portal["detail"] = "两者均需 Portal 认证，请注意认证页面真伪"
    dimensions.append(dim_portal)

    # ── 综合评分与建议 ──
    score_a = _calc_score(wifi_a)
    score_b = _calc_score(wifi_b)

    win_count_a = sum(1 for d in dimensions if d["winner"] == "A")
    win_count_b = sum(1 for d in dimensions if d["winner"] == "B")

    if score_a > score_b:
        recommendation = "A"
        summary = (
            f"综合 5 个维度对比，**{wifi_a['ssid']}** 在 {win_count_a} 个维度上表现更优"
            f"（综合评分 {score_a} vs {score_b}），建议优先连接此网络。"
        )
    elif score_b > score_a:
        recommendation = "B"
        summary = (
            f"综合 5 个维度对比，**{wifi_b['ssid']}** 在 {win_count_b} 个维度上表现更优"
            f"（综合评分 {score_b} vs {score_a}），建议优先连接此网络。"
        )
    else:
        recommendation = "持平"
        summary = (
            f"两者综合评分相同（均为 {score_a} 分），安全性相当。"
            f"可根据信号稳定性或个人偏好选择连接。"
        )

    return {
        "ssid_a": wifi_a["ssid"],
        "ssid_b": wifi_b["ssid"],
        "score_a": score_a,
        "score_b": score_b,
        "dimensions": dimensions,
        "recommendation": recommendation,
        "summary": summary,
    }
