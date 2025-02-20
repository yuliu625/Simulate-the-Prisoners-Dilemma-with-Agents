from autogen_ext.models.openai import OpenAIChatCompletionClient

import os
from enum import Enum


class QwenModelName(Enum):
    qwen_15 = 'qwen2.5-1.5b-instruct'


def get_qwen(model: str = 'qwen2.5-1.5b-instruct'):
    model_client = OpenAIChatCompletionClient(
        model=model,
        base_url=os.environ['OPENAI_COMPATIBILITY_API_BASE_URL'],
        api_key=os.environ['OPENAI_COMPATIBILITY_API_KEY'],
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": False,
            "family": 'unknown',
        },
    )
    return model_client


if __name__ == '__main__':
    pass
