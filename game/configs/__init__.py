"""
agent和game的设置。修改这个包，以供runtime包进行设置和进行实验。

收集prompts包配置，可复用。可视为序列化文件。
"""

__all__ = [
    'get_manager_config',
    'get_participant_config'
]

from .manager_config import get_manager_config
from .participant_config import get_participant_config
