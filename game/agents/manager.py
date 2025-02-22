"""
关于manager的设定。

这里，不需要基于LLM的manager，基于固定算法的设定会更可靠。
"""

from game.protocols import GameSetting, GameRequest, ManagerRequest, ParticipantChoice

from autogen_core import (
    RoutedAgent,
    MessageContext,
    AgentId,
    message_handler,
)

import re
import json
from pathlib import Path

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
        description: str,
        participant_ids: List[AgentId],
        game_rules: dict,  # 游戏规则，例如选择、payoff
        game_setting: dict,  # 为了保存游戏的设置
    ):
        super().__init__(description)
        self._game_rules = game_rules
        self._game_setting = game_setting
        self._participant_ids = participant_ids
        # 过去所有agent的对话。
        self._game_context = []
        # 解析对话后，模型JSON格式的想法。但这并不会给participant展示。
        self._game_thoughts = {}
        # 解析和计算后，participant的选择和收益。
        self._game_history = {}

    @message_handler
    async def on_game_request(self, message: GameRequest, context: MessageContext) -> None:
        """设置试验，进行试验。"""
        # 进行多轮试验。
        for game_round in range(1, message.game_round+1):
            print(f"第{game_round}轮实验：")
            await self.run_a_round(
                game_round=game_round,
                participant_message_template=message.participant_message_template,
                history_prompt_template=message.history_prompt_template,
            )
        # 完成实验之后保存设置和结果。
        # self.save_result()

    async def run_a_round(
        self,
        game_round: int,
        participant_message_template: str,
        history_prompt_template: str,
    ) -> dict:
        """运行一轮实验。"""
        # 给每一个participant发送消息。
        participant_message_content = participant_message_template.format(game_round=game_round)
        if game_round > 1:
            history_prompt_content = history_prompt_template.format(choice_and_payoff_history=self._game_history)
            participant_message_content = history_prompt_content + participant_message_content
        # 记录所有participant的想法。
        participant_thoughts = {}
        # 记录所有agent的选择。逐步记录，因为在所有agent完成选择之后才能计算结果。
        participant_choices = {}
        for i, participant_id in enumerate(self._participant_ids):
            participant_response: ParticipantChoice = await self.send_message_to_participant(
                participant_message_content=participant_message_content,
                participant_id=participant_id,
            )
            # 记录agent响应。
            self._game_context.append({f'{participant_id.key}': participant_response.content})
            # 记录participant的思考
            participant_thoughts[participant_id.key] = participant_response.result
            # 记录participant的选择。单独提取是为了计算。
            participant_choices[participant_id.key] = {'choice': participant_response.result['choice']}
        # 当所有的participant完成选择，计算结果
        round_result = self._calculate_payoff(participant_choices)
        # 记录结果。
        self._game_thoughts[f"{game_round}"] = participant_thoughts
        self._game_history[f"{game_round}"] = round_result
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
        raw_data_str: str = matches[-1]
        return json.loads(raw_data_str)

    def _calculate_payoff(self, participant_choices: dict) -> dict:
        all_choice = ""
        for participant_id, choice_dict in participant_choices.items():
            all_choice += f"{choice_dict['choice']}_"
        all_choice = all_choice[:-1]
        payoff_list = self._game_rules['payoffs'][all_choice]
        for i, (participant_id, choice_dict) in enumerate(participant_choices.items()):
            participant_choices[participant_id]['payoff'] = payoff_list[i]
        return participant_choices

    def save_result(self, dir_to_save: str) -> None:
        dir_to_save = Path(dir_to_save)
        with open(dir_to_save / 'game_rules.json', 'w', encoding='utf-8') as f:
            json.dump(self._game_rules, f, ensure_ascii=False, indent=4)
        with open(dir_to_save / 'game_context.json', 'w', encoding='utf-8') as f:
            json.dump(self._game_context, f, ensure_ascii=False, indent=4)
        with open(dir_to_save / 'game_thoughts.json', 'w', encoding='utf-8') as f:
            json.dump(self._game_thoughts, f, ensure_ascii=False, indent=4)
        with open(dir_to_save / 'game_history.json', 'w', encoding='utf-8') as f:
            json.dump(self._game_history, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    pass
