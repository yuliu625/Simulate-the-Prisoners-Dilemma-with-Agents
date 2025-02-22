"""
dict形式的试验控制者的设置。
"""

from game.prompts import get_participant_system_prompt_template

from autogen_core import AgentId

from typing import TypedDict


class ManagerConfig(TypedDict):
    description: str
    participant_ids: list[AgentId]
    game_rule: dict
    game_setting: dict


class GameRule(TypedDict):
    players: list[str]
    strategies: list[list[str]]
    payoffs: dict[str, list[int]]


class GameSetting(TypedDict):
    participant_system_prompt: str
    dir_to_save: str


def get_manager_config() -> ManagerConfig:
    return dict(
        description="一场实验的控制者。",
        participant_ids=[AgentId(type='participant', key='Player1'), AgentId(type='participant', key='Player2'),],
        game_rule=dict(
            players=['Player1', 'Player2'],
            strategies=[
                [],
                [],
            ],
            payoffs={

            }
        ),
        game_setting=dict(
            participant_system_prompt=get_participant_system_prompt_template(
                participant_system_prompt=None,
                game_description=None,
                participant_description=None,
                response_format=None,
            ),
            dir_to_save=r"",
        )
    )


if __name__ == '__main__':
    print(get_manager_config())
