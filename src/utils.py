"""
数据加载与辅助工具函数模块。
"""

import json
import os
from typing import List, Dict, Any


# 根据项目结构自动定位 data 目录
def _get_data_path() -> str:
    """获取 wifi_scenarios.json 的绝对路径。"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    return os.path.join(project_root, "data", "wifi_scenarios.json")


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
