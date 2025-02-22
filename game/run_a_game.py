"""
根据设置，运行一次试验。
"""

from game.runtime import GameRunner
from game.prompts import (
    get_participant_system_prompt_template,
    get_history_prompt_template,
    get_participant_message_prompt_template,
)
from game.protocols import GameRequest


async def run_game():
    game_runner = GameRunner(
        manager_config={},
        participant_config={}
    )

    await game_runner.run_a_game(
        GameRequest(
            game_round=1,
            participant_message_template="",
            history_prompt_template=""
        )
    )


if __name__ == '__main__':
    pass
