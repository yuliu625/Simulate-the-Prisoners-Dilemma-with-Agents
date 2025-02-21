"""
根据设置，运行一次试验。
"""

from game.agents import Manager, Participant
from game.protocols import GameSetting

from autogen_core import SingleThreadedAgentRuntime
from autogen_ext.models.openai import OpenAIChatCompletionClient

from autogen_core import AgentId

from typing import List


class GameRunner:
    def __init__(self, model_client: OpenAIChatCompletionClient):
        self.runtime = self._init_runtime()
        self._model_client = model_client
        self._participant_ids = []

    def _init_runtime(self):
        return SingleThreadedAgentRuntime()

    async def register_agents(self, participant_ids: List[AgentId]):
        """
        注册相关的agent。
        """
        await Manager.register(
            self.runtime,
            type='manager',
            factory=lambda: Manager(
                participant_ids=participant_ids
            )
        )
        await Participant.register(
            self.runtime,
            type='participant',
            factory=lambda: Participant(
                '试验的参与者。', self._model_client
            )
        )

    async def run_a_game(self, setting):
        self.runtime.start()
        await self.runtime.send_message(

        )
        await self.runtime.stop_when_idle()


if __name__ == '__main__':
    pass
