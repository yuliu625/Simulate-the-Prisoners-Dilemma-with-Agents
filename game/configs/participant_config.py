"""
dict形式的试验参与者的设置。
"""

from game.configs._model_client import get_qwen, QwenModelName
from game.prompts import get_participant_system_prompt_template

from autogen_ext.models.openai import OpenAIChatCompletionClient

from typing import TypedDict


class ParticipantConfig(TypedDict):
    description: str
    model_client: OpenAIChatCompletionClient
    system_prompt_template: str


def get_participant_config() -> ParticipantConfig:
    return dict(
        description="一个实验的参与者",
        model_client=get_qwen(QwenModelName.qwen_15.value),
        system_prompt_template=get_participant_system_prompt_template(
            participant_system_prompt=None,
            game_description=None,
            participant_description=None,
            response_format=None,
        )
    )


if __name__ == '__main__':
    print(get_participant_config())
