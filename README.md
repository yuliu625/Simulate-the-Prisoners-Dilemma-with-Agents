# Simulating the Prisoner's Dilemma with Agents

## Project Overview
This project is a game theory simulation based on the **AutoGen** framework, designed to explore the classic **Prisoner's Dilemma** using **Large Language Model (LLM)-driven agents**.

By fully simulating this game, we can deeply investigate the decision-making behavior of LLM agents in various scenarios. This project features a highly flexible configuration, allowing you to easily adjust various experimental parameters, including:

- **Payoff Matrix**: Define the rewards and penalties for the game.
- **Agent Behavior**: Define the agents' roles, identities, and decision-making styles.
- **Simulation Steps**: Fine-tune every step of the experiment.

The results of each experiment are logged for further analysis.


## Core Components
The project has a clear structure, with the core code located in the `game` directory.
- **`agents`**: Defines two core agents:
  - **`Participant`**: Plays the role of the prisoner, and their behavior and decisions are the focus of the experiment.
  - **`Manager`**: Responsible for coordinating and running the entire experiment, as well as logging the results.
- **`configs`**: Centralizes all experimental configurations. I used Python objects and `TypeDict` to declare the configuration fields, making them easy to modify. Additionally, prompt templates support dynamic generation, allowing you to customize prompts by modifying `kwargs` to control agent behavior.
- **`prompts`**: Contains all prompt-related files. Although there are many templates, the core logic is concentrated in `participant_prompts.py`, which encapsulates complex string processing to make prompt modification simple and efficient.
- **`protocols`**: Defines the communication protocols between agents. We use `dataclass` for a simple structure that's easy to understand and modify.
- **`runtime`**: Encapsulates the AutoGen runtime object, providing a simple and easy-to-use runner.
- **`utils`**: Includes various utility functions, such as processing f-strings and converting JSON data.


## How to Run
Start your experiment in just two steps:

### 1. Configure the Experiment
In the `configs` directory, you can adjust the following files as needed:
- **`_model_client.py`**: Configure your model client. It supports **Tongyi Qianwen (Qwen)** by default, but you can add a custom factory method to use other OpenAI client-compatible models.
- **`game_request.py`**: Adjust game settings, such as the number of experimental rounds, and batch modify prompt templates.
- **`manager_config.py`**: Set game rules, the number of participants, and the result storage path.
- **`participant_config.py`**: Change the underlying LLM model, identity settings, and reasoning style for each participant.

All configurations have default values, so you can run the code directly without any changes.

### 2. Run the Code
Run `run_a_game.py` from the command line. You will see the real-time output of the experiment. The experimental results will be automatically saved to the directory you specified in the configuration.


## Interesting Findings
During the simulation of the Prisoner's Dilemma, I observed that LLM agents exhibit many **human-like behaviors**. As long as clear instructions are provided, they display complex and diverse decision-making patterns.

- **Strategic Evolution**: In multi-round experiments, agents adjust their strategies based on the opponent's behavior.
- **Behavioral Economics**: They demonstrate various complex behaviors, such as choosing to cooperate or defect in different situations, which aligns with certain strategies in behavioral economics.
- **Cooperative Tendency**: Most agents tend to be **cooperative**. This may be due to the data used to train LLMs, which promotes a friendly and collaborative disposition. However, "smarter" or more "creative" agents are more likely to **defect** to maximize their own interests.

These findings suggest that the behavior of LLM agents is not entirely rational. In many aspects, their decisions are similar to human decision-making, providing a new perspective for studying the social behavior of LLMs.


## Future Outlook
This project has room for improvement, and your contributions are welcome!
- **Communication Method**: Currently, direct invocation is used. We can explore a more efficient broadcast communication mechanism in the future.
- **Configuration Optimization**: Further simplify the configuration process to lower the barrier to use.
- **Logging System**: Explore more robust and flexible logging solutions, such as using AutoGen's built-in `ClosureAgent` or other superior implementations.

If you have any ideas or suggestions for this project, feel free to submit an Issue or a Pull Request.


## Other Projects
If you are interested in game theory or LLM-based agents, you can check out my other projects:
- [Agent-Development-Toolkit](https://github.com/yuliu625/Yu-Agent-Development-Toolkit): A general toolkit I built for agent development.
- [World-of-Six](https://github.com/yuliu625/World-of-Six): A study on the behavior of LLM-based agents in a complex game theory scenario. This is the repository for my conference paper accepted by **SWAIB[2025]**.
- **Not yet open-sourced**: I currently have a working paper on the expected behavior of LLM-based agents in environments with network effects. The corresponding code repository will be open-sourced after the journal submission is accepted.

