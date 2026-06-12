"""
数据加载与辅助工具函数模块。
"""

import json
import os
from typing import List, Dict, Any


def _get_data_path() -> str:
    """获取 wifi_scenarios.json 的绝对路径。"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    return os.path.join(project_root, "data", "wifi_scenarios.json")


def _get_feedback_path() -> str:
    """获取 user_feedback.json 的绝对路径。"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    return os.path.join(project_root, "data", "user_feedback.json")


def load_mock_data() -> List[Dict[str, Any]]:
    """从本地 JSON 文件加载模拟 WiFi 场景数据。

    Returns:
        WiFi 节点列表，每个节点为一个包含 ssid、加密方式等字段的字典。

    Raises:
        FileNotFoundError: JSON 文件不存在时抛出。
        ValueError: JSON 格式错误或数据为空时抛出。
    """
    data_path = _get_data_path()

    if not os.path.exists(data_path):
        raise FileNotFoundError(
            f"⚠️ 模拟数据文件未找到: {data_path}\n"
            f"请确保 '{os.path.basename(data_path)}' 文件已放置在 data/ 目录下。"
        )

    try:
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"⚠️ JSON 文件格式错误，无法解析: {e}")

    wifi_nodes = data.get("wifi_nodes", [])
    if not wifi_nodes:
        raise ValueError("⚠️ 未扫描到任何 WiFi 信号（模拟数据为空）。")

    return wifi_nodes


def _get_blacklist_notes_path() -> str:
    """获取 blacklist_notes.json 的绝对路径。"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    return os.path.join(project_root, "data", "blacklist_notes.json")


def load_blacklist_notes() -> Dict[str, str]:
    """从本地 JSON 文件加载黑名单备注数据。

    Returns:
        {wifi_uid: note_text} 映射字典，文件不存在时返回空字典。
    """
    path = _get_blacklist_notes_path()
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data
        return {}
    except (json.JSONDecodeError, IOError):
        return {}


def save_blacklist_notes(notes: Dict[str, str]) -> bool:
    """保存黑名单备注到本地 JSON 文件。

    Args:
        notes: {wifi_uid: note_text} 映射字典。

    Returns:
        True 表示保存成功，False 表示保存失败。
    """
    path = _get_blacklist_notes_path()
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(notes, f, ensure_ascii=False, indent=2)
        return True
    except IOError:
        return False


def save_feedback(text: str) -> bool:
    """保存用户反馈到本地 JSON 文件。

    Args:
        text: 用户输入的反馈文本。

    Returns:
        True 表示保存成功，False 表示保存失败。
    """
    from datetime import datetime

    feedback_path = _get_feedback_path()
    try:
        existing = []
        if os.path.exists(feedback_path):
            with open(feedback_path, "r", encoding="utf-8") as f:
                existing = json.load(f)
    except (json.JSONDecodeError, IOError):
        existing = []

    existing.append({
        "timestamp": datetime.now().isoformat(),
        "content": text.strip(),
    })

    try:
        os.makedirs(os.path.dirname(feedback_path), exist_ok=True)
        with open(feedback_path, "w", encoding="utf-8") as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)
        return True
    except IOError:
        return False
