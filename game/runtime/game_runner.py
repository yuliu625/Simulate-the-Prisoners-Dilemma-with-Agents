"""
根据设置，运行一次试验。
"""

from game.agents import Manager, Participant
from game.protocols import GameRequest
from game.prompts import (
    get_participant_system_prompt_template,
    get_history_prompt_template,
    get_participant_message_prompt_template,
)

from autogen_core import SingleThreadedAgentRuntime

from autogen_core import AgentId


class GameRunner:
    def __init__(self, manager_config: dict, participant_config: dict):
        self._manager_config = manager_config
        self._participant_config = participant_config

        self.runtime = self._init_runtime()
        self._register_agents()

    def _init_runtime(self):
        return SingleThreadedAgentRuntime()

    async def _register_agents(self):
        """
        注册相关的agent。
        """
        await Manager.register(
            self.runtime,
            type='manager',
            factory=lambda: Manager(
                **self._manager_config,
            )
        )
        await Participant.register(
            self.runtime,
            type='participant',
            factory=lambda: Participant(
                **self._participant_config,
            )
        )

    async def run_a_game(self, game_request: GameRequest):
        self.runtime.start()
        await self.runtime.send_message(
            message=game_request,
            recipient=AgentId(type='manager', key='default')
        )
        await self.runtime.stop_when_idle()


if __name__ == '__main__':
    pass
