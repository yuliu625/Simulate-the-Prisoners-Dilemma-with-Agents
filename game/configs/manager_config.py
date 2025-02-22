"""
dict形式的试验控制者的设置。
"""

from autogen_core import AgentId


manager_config = dict(
    description="一场实验的控制者。",
    participant_ids=[AgentId(type='participant', key='Player1'), AgentId(type='participant', key='Player2'),],
    game_rules={},
    game_setting={}
)


if __name__ == '__main__':
    pass
