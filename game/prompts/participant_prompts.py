"""
以函数化的方式规范prompt template的获取。

所以的结果都可以执行format方法而不出错。
"""

from game.utils import escape_braces, json_escape_braces


def _escape_braces(string) -> str:
    # 先将所有的 { } 替换为 {{ }}，然后再处理单独的 { 或者 }
    string = string.replace("{", "{{").replace("}", "}}")
    return string


def get_participant_system_prompt_template(
    participant_system_prompt: str = None,
    game_description: str = None,
    participant_description: str = None,
    game_setting: dict = None,
    response_format: str = None,
) -> str:
    participant_system_prompt = """\
你现在要进行角色扮演：
{game_description}

参与者的情况是：
{participants_description}

{response_format}

游戏的设置是：
{game_setting}

你需要一直记住你的身份是：
""" if participant_system_prompt is None else participant_system_prompt

    game_description = """\
你正在和另一名参与者参加一场囚徒困境的实验，你是其中一名参与者。\
""" if game_description is None else game_description

    participant_description = """\
所有参与者都足够理性，并且追求自己最大的收益。\
""" if participant_description is None else participant_description

    game_setting = """\
```json
{
  "players": ["player1", "player2"],
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
```""" if game_setting is None else json_escape_braces(game_setting)

    response_format = """\
你必须以markdown代码块包裹的JSON格式返回你的选择，例如：
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
```""" if response_format is None else response_format

    result = participant_system_prompt.format(
        game_description=game_description,
        participants_description=participant_description,
        game_setting=game_setting,
        response_format=response_format,
    )
    result = escape_braces(result)
    return result + '{role}'


def get_participant_message_prompt_template(
    game_round: int = None
) -> str:
    participant_message_prompt_template = """\
现在是第{game_round}轮试验。

接下来，逐步思考以下问题：
1. 你对于目前游戏的状态是如何分析的。
2. 你预期其他参与者会如何做出选择。
3. 你打算做出的选择，以及做出这个选择的原因。

最后，你以JSON格式返回你的选择。
现在，开始逐步思考，然后做出你的选择。
"""
    return participant_message_prompt_template


def get_history_prompt_template(
    choice_and_payoff_history: dict = None,
) -> str:
    history_prompt_template = """\
在过去，所有玩家的选择和收益是：
{choice_and_payoff_history}
"""
    return history_prompt_template


def get_participant_inference_prompt_template(
    participant_inference_prompt_template: str = None,
    choice_and_payoff_history: dict = None,
) -> str:
    participant_inference_prompt_template = """\
在过去，所有玩家的选择和收益是：
{choice_and_payoff_history}

现在是第{game_round}轮试验。

接下来，逐步思考以下问题：
1. 你对于目前游戏的状态是如何分析的。
2. 你预期其他参与者会如何做出选择。
3. 你打算做出的选择，以及做出这个选择的原因。

最后，你以JSON格式返回你的选择。
现在，开始逐步思考，然后做出你的选择。
""" if participant_inference_prompt_template is None else participant_inference_prompt_template

    if choice_and_payoff_history is None:
        participant_inference_prompt_template = """\
现在是第{game_round}轮试验，

接下来，逐步思考以下问题：
1. 你对于目前游戏的状态是如何分析的。
2. 你预期其他参与者会如何做出选择。
3. 你打算做出的选择，以及做出这个选择的原因。

最后，你以JSON格式返回你的选择。
现在，开始逐步思考，然后做出你的选择。
"""
        return participant_inference_prompt_template

    choice_and_payoff_history: str = json_escape_braces(choice_and_payoff_history)
    choice_and_payoff_history = escape_braces(choice_and_payoff_history)
    result = participant_inference_prompt_template.format(
        choice_and_payoff_history=choice_and_payoff_history,
        game_round='{game_round}',
    )
    return result


if __name__ == '__main__':
    # print(get_participant_system_prompt_template().format(role='player1'))
#     print(get_participant_inference_prompt_template(choice_and_payoff_history={
#     "第1轮": {"玩家 1": {"选择": "背叛", "收益": "5"}, "玩家 2": {"选择": "合作", "收益": "0"}},
#     "第2轮": {"玩家 1": {"选择": "背叛", "收益": "5"}, "玩家 2": {"选择": "合作", "收益": "0"}},
#     "第3轮": {"玩家 1": {"选择": "背叛", "收益": "5"}, "玩家 2": {"选择": "合作", "收益": "0"}},
#     "第4轮": {"玩家 1": {"选择": "背叛", "收益": "5"}, "玩家 2": {"选择": "合作", "收益": "0"}},
#     "第5轮": {"玩家 1": {"选择": "背叛", "收益": "5"}, "玩家 2": {"选择": "合作", "收益": "0"}},
# }).format(game_round=5))
    print(get_participant_message_prompt_template().format(game_round=0))
#     print(get_history_prompt_template().format(choice_and_payoff_history={
#     "第1轮": {"玩家 1": {"选择": "背叛", "收益": "5"}, "玩家 2": {"选择": "合作", "收益": "0"}},
#     "第2轮": {"玩家 1": {"选择": "背叛", "收益": "5"}, "玩家 2": {"选择": "合作", "收益": "0"}},
#     "第3轮": {"玩家 1": {"选择": "背叛", "收益": "5"}, "玩家 2": {"选择": "合作", "收益": "0"}},
#     "第4轮": {"玩家 1": {"选择": "背叛", "收益": "5"}, "玩家 2": {"选择": "合作", "收益": "0"}},
#     "第5轮": {"玩家 1": {"选择": "背叛", "收益": "5"}, "玩家 2": {"选择": "合作", "收益": "0"}},
# }))
