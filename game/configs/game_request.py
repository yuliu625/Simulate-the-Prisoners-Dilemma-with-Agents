"""
获取game request对象的工程。

暂时使用硬编码，在这个文件中进行修改。因为复杂的配置，这样或许更方便。
"""

from game.prompts import get_history_prompt_template, get_participant_message_prompt_template


def get_game_request():
    return dict(
        game_round=1,
        participant_message_template=get_participant_message_prompt_template(
            participant_message_prompt_template=None
        ),
        history_prompt_template=get_history_prompt_template(
            history_prompt_template=None
        )
    )


if __name__ == '__main__':
    print(get_game_request())
