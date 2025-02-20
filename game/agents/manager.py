"""
关于manager的设定。

这里，不需要基于LLM的manager，基于固定算法的设定会更可靠。
"""

from game.protocols import GameSetting, ManagerRequest, ParticipantChoice

from autogen_core import (
    RoutedAgent,
    MessageContext,
    AgentId,
    message_handler
)

import re
import json

from typing import List


class Manager(RoutedAgent):
    """
    一轮试验的控制者。
    会进行：
        - 初始化游戏设定。
        - 进行每一轮试验。
        - 收集试验结果。
    """
    def __init__(
        self,
        participant_ids: List[AgentId],
        game_round: int = 10,
    ):
        super().__init__('控制一场试验的管理者。')
        self._game_round = game_round
        self._participant_ids = participant_ids
        self._game_context = []
        self._game_history = {}
        self._game_thoughts = {}

    @message_handler
    async def on_game_setting(self, message: GameSetting, context: MessageContext) -> None:
        """设置试验，进行试验。"""
        system_prompt_template = message.system_prompt_template
        inference_prompt_template = message.inference_prompt_template
        # 进行多轮试验。
        for game_round in range(self._game_round):
            await self.run_a_round()

    async def run_a_round(self, game_round: int, ) -> dict:
        """运行一轮实验。"""
        # 给每一个participant发送消息。
        participant_choices = {}
        participant_thoughts = {}
        for i, participant_id in enumerate(self._participant_ids):
            participant_response: ParticipantChoice = await self.send_message_to_participant()
            # 记录和解析结果。
            self._game_context.append({f'{participant_id.key}': participant_response.content})
            # 记录participant的思考
            participant_thoughts[participant_id.key] = participant_response.result
            # 记录participant的选择
            participant_choices[participant_id.key] = participant_response.result['choice']
        # 当所有的participant完成选择，计算结果
        round_result = self._calculate_profit(participant_choices)
        # 记录结果。
        self._game_history.append(round_result)
        return round_result

    async def send_message_to_participant(self, participant_message_content: str, participant_id: AgentId) -> ParticipantChoice:
        """
        向一个participant发送一条请求。
        这个方法应独立于manager的逻辑，manager对于请求的内容自行处理。这个方法是为了保持2个agent的通讯协议。
        """
        participant_response: ParticipantChoice = await self.send_message(
            message=ManagerRequest(
                content=participant_message_content,
            ),
            recipient=participant_id,
        )
        return participant_response

    def _extract_json_response(self, response: str) -> dict | None:
        pattern = r'```json(.*?)```'
        matches = re.findall(pattern, response, re.DOTALL)
        if not matches:
            return None
        raw_data_str: str = matches[0]
        return json.loads(raw_data_str)

    def _calculate_profit(self, choice: dict) -> dict:
        ...


if __name__ == '__main__':
    pass
