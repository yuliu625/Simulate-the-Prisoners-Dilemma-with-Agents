"""
agent之间通讯的协议。
"""

from dataclasses import dataclass


@dataclass
class GameRequest:
    game_round: int
    participant_message_template: str
    history_prompt_template: str


@dataclass
class ManagerRequest:
    # system_prompt: str
    content: str
    # game_round: int


@dataclass
class ParticipantChoice:
    content: str
    result: dict
    # choice: str
    # analysis: str
    # expectation: str
    # reason: str


@dataclass
class ParsedResult:
    choice: str
    analysis: str
    expectation: str
    reason: str


if __name__ == '__main__':
    pass
