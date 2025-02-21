"""
试验参与者的设定。

尽可能详尽设置，保证试验的复用性。
"""

from game.protocols import ManagerRequest, ParticipantChoice

from autogen_core import (
    RoutedAgent,
    MessageContext,
    message_handler
)
from autogen_core.models import (
    SystemMessage,
    AssistantMessage,
    UserMessage,
    LLMMessage
)
from autogen_core.model_context import UnboundedChatCompletionContext, BufferedChatCompletionContext
from autogen_ext.models.openai import OpenAIChatCompletionClient

import re
import json

_PARTICIPANT_MAX_RETRIES = 10


class Participant(RoutedAgent):
    """
    试验的参与者。
    可以进行：
        - 分析之前试验的结果。
        - 做出预期。
        - 返回结构化的分析和选择结果。
    """
    def __init__(
        self,
        description: str,
        model_client: OpenAIChatCompletionClient,
        system_prompt_template: str,
        # inference_prompt_template: str,
    ):
        super().__init__(description)
        self._model_client = model_client
        self._model_context = BufferedChatCompletionContext(buffer_size=10)
        self._system_prompts: list[LLMMessage] = [SystemMessage(content=system_prompt_template.format(role=self.id.key))]
        # self._inference_prompt_template: str = inference_prompt_template

    @message_handler
    async def on_manager_request(self, message: ManagerRequest, context: MessageContext) -> ParticipantChoice:
        print(f"{self.id.key}进行选择")
        # 维护模型上下文。
        await self._model_context.add_message(UserMessage(content=message.content, source='manager'))
        # 调用LLM进行响应。
        response = ""
        for i in range(_PARTICIPANT_MAX_RETRIES):
            # print(f"第{i}次尝试生成。")
            # 进行最多10次尝试，需要返回的结果是符合通讯协议的。
            response = await self.request_llm(message, context)
            # print(response)
            result = self._extract_json_response(response)
            if result:
                break
        # 维护模型上下文。
        await self._model_context.add_message(AssistantMessage(content=response, source=self.id.key))
        # 返回manager可解析的协议数据。
        return ParticipantChoice(
            content=response,
            result=self._extract_json_response(response)
        )

    async def request_llm(self, message: ManagerRequest, context: MessageContext) -> str:
        llm_result = await self._model_client.create(
            messages=self._system_prompts + await self._model_context.get_messages(),
            cancellation_token=context.cancellation_token
        )
        response: str = llm_result.content
        return response

    def _extract_json_response(self, response: str) -> dict | None:
        pattern = r'```json(.*?)```'
        matches = re.findall(pattern, response, re.DOTALL)
        if not matches:
            return None
        raw_data_str: str = matches[-1]
        return json.loads(raw_data_str)


if __name__ == '__main__':
    from autogen_ext.models.openai import OpenAIChatCompletionClient
    import os

    model_client = OpenAIChatCompletionClient(
        model='qwen2.5-1.5b-instruct',
        base_url=os.environ['OPENAI_COMPATIBILITY_API_BASE_URL'],
        api_key=os.environ['OPENAI_COMPATIBILITY_API_KEY'],
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": False,
            "family": 'unknown',
        },
    )

    from autogen_core import SingleThreadedAgentRuntime
    from autogen_core import AgentId

    async def run_demo():
        runtime = SingleThreadedAgentRuntime()
        await Participant.register(
            runtime,
            type='participant',
            factory=lambda: Participant(
                '试验的参与者。',
                model_client=model_client,
                system_prompt_template="你是一个好帮手。"
            )
        )
        runtime.start()
        response = await runtime.send_message(
            message=ManagerRequest(
                content="返回一个markdown中代码块包裹的json数据，包含字段为['choice', 'analysis', 'expectation', 'reason']",
            ),
            recipient=AgentId(type='participant', key='agent-1'),
        )
        print(response)
        await runtime.stop_when_idle()

    import asyncio
    # asyncio.run(run_demo())

    async def run_a_choice():
        runtime = SingleThreadedAgentRuntime()
        await Participant.register(
            runtime,
            type='participant',
            factory=lambda: Participant(
                '试验的参与者。',
                model_client=model_client,
                system_prompt_template="""\
你正在和另一名参与者参加一场囚徒困境的实验，你是其中一名参与者。

游戏的设置是：
```json
{
  "players": ["玩家 1", "玩家 2"],
  "strategies": [
    ["合作", "背叛"],
    ["合作", "背叛"]
  ],
  "payoffs": {
    "合作_合作": [3, 3],
    "合作_背叛": [0, 5],
    "背叛_合作": [5, 0],
    "背叛_背叛": [1, 1]
  }
}
```

另一名参与者的情况是：
和你一样的agent的，你们都会追求自身的最大收益。

你的身份是：
玩家1

你必须以JSON格式返回你的选择，例如：
```json
{
    "choice": "合作"，
    "analysis": "目前游戏处于一种均衡状态，并且长期考虑可以维持。",
    "expectation": "我预期另一个参与者会合作。",
    "reason": "上一轮的合作我们获得了更高的收益，我应该这轮选择继续合作。"
}
```
或者
```json
{
    "choice": "背叛"，
    "analysis": "目前游戏处于一种均衡状态，但是我改变选择可以获得更高的收益。",
    "expectation": "我预期另一个参与者会合作。",
    "reason": "我可以通过背叛获得更高的收益。"
}
```"""
            )
        )
        runtime.start()
        response = await runtime.send_message(
            message=ManagerRequest(
                content="""\
现在是第{game_round}轮试验，

接下来，逐步思考以下问题：
1. 你对于目前游戏的状态是如何分析的。
2. 你预期其他参与者会如何做出选择。
3. 你打算做出的选择，以及做出这个选择的原因。

最后，你以JSON格式返回你的选择。
现在，开始逐步思考，然后做出你的选择。""",
            ),
            recipient=AgentId(type='participant', key='agent-1'),
        )
        print(response)
        await runtime.stop_when_idle()

    import asyncio
    asyncio.run(run_a_choice())
