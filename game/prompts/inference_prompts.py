"""
引导agent做出选择的prompt。
"""

participant_user_prompt = """\
现在是第{game_round}轮试验，

接下来，逐步思考以下问题：
1. 你对于目前游戏的状态是如何分析的。
2. 你预期其他参与者会如何做出选择。
3. 你打算做出的选择，以及做出这个选择的原因。

最后，你以JSON格式返回你的选择，例如：
```json
{
    "choice": "合作"，
    "analysis": "我觉得其他参与者会选择合作，",
    "expectation": "我预期其他参与者",
    "reason": "上一轮的合作我们获得了更高的收益，我应该这轮选择继续合作。"
}
```

现在，做出你的选择。"""

participant_user_prompt_with_history = """\

"""

inference_prompt_template = """\
现在是第{game_round}轮试验，

接下来，逐步思考以下问题：
1. 你对于目前游戏的状态是如何分析的。
2. 你预期其他参与者会如何做出选择。
3. 你打算做出的选择，以及做出这个选择的原因。

最后，你以JSON格式返回你的选择。
现在，开始逐步思考，然后做出你的选择。"""

history_prompt_template = """\
在过去，所有玩家的选择和收益是：
{choice_and_payoff_history}
"""


if __name__ == '__main__':
    pass
