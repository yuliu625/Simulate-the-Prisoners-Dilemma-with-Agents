"""
agent的system prompt，
给出agent的身份，引导进行选择。
"""

__all__ = [
    'get_participant_system_prompt_template',
    'get_history_prompt_template',
    'get_participant_message_prompt_template'
]

from .participant_prompts import (
    get_participant_system_prompt_template,
    get_history_prompt_template,
    get_participant_message_prompt_template,
)

