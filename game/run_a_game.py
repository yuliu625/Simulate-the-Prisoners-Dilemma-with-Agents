"""
根据设置，运行一次试验。
"""

from game.runtime import GameRunner
from game.prompts import (
    get_history_prompt_template,
    get_participant_message_prompt_template,
)
from game.protocols import GameRequest
from game.configs import get_manager_config, get_participant_config

import asyncio


async def run_game(game_round: int = 1):
    """
    运行实验。
    设置相关的内容需要到configs中进行修改。
    """
    game_runner = GameRunner(
        manager_config=get_manager_config(),
        participant_config=get_participant_config(),
    )

    await game_runner.run_a_game(
        GameRequest(
            game_round=game_round,
            participant_message_template=get_participant_message_prompt_template(
                participant_message_prompt_template=None
            ),
            history_prompt_template=get_history_prompt_template(
                history_prompt_template=None
            ),
        )
    )


if __name__ == '__main__':
    asyncio.run(run_game())
