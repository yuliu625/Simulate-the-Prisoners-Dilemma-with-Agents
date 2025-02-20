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
        system_prompt: str,
        inference_prompt_template: str,
    ):
        super().__init__(description)
        self._model_client = model_client
        self._model_context = BufferedChatCompletionContext(buffer_size=10)
        self._system_prompts: list[LLMMessage] = [SystemMessage(content=system_prompt.format(role=self.id.key))]
        self._inference_prompt_template: str = inference_prompt_template

    @message_handler
    async def on_manager_request(self, message: ManagerRequest, context: MessageContext) -> ParticipantChoice:
        print(f"{self.id.key}进行选择")
        # 维护模型上下文。
        await self._model_context.add_message(UserMessage(content=message.content, source='manager'))
        # 调用LLM进行响应。
        response = ""
        for i in range(10):
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
            factory=lambda: Participant('试验的参与者。', model_client)
        )
        runtime.start()
        response = await runtime.send_message(
            message=ManagerRequest(
                system_prompt="你是一个好帮手。",
                content="返回一个markdown中代码块包裹的json数据，包含字段为['choice', 'analysis', 'expectation', 'reason']",
                game_round=1
            ),
            recipient=AgentId(type='participant', key='agent-1'),
        )
        print(response)
        await runtime.stop_when_idle()

    import asyncio
    asyncio.run(run_demo())
