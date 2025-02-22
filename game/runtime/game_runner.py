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
                participant_ids=participant_ids,
                game_rules={}
            )
        )
        await Participant.register(
            self.runtime,
            type='participant',
            factory=lambda: Participant(
                '试验的参与者。',
                model_client=self._model_client,
                system_prompt_template=get_participant_system_prompt_template()
            )
        )

    async def run_a_game(self, setting):
        self.runtime.start()
        await self.runtime.send_message(
            message=GameRequest(

            ),
            recipient=AgentId()
        )
        await self.runtime.stop_when_idle()


if __name__ == '__main__':
    pass
