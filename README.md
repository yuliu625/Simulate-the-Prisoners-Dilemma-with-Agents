# Simulate the Prisoner's Dilemma with Agents

## Overview
Code for a game theory simulation experiment based on the autogen framework. The Prisoner's Dilemma is implemented here.

I have implemented a complete simulation of the prisoner's Dilemma and provide a very flexible way to configure it. (In fact, it may be too complex, make it difficult.) It is possible to change the payoff matrix, the equilibrium goal, the agent's behavior, and specifically each step of the simulation.

The code can be run to perform a large number of simulation experiments with different settings for LLM-based agents. The results are all documented after each experiment is completed.

## Component
### game
This is the root directory of the project. The other folders are documents and results.
#### agents
I define and build two agents. 
- `Participant` is a good enough implementation that this agent can simulate many participants of multiple experiments.
- `Manager` is the manager of the experiment and is responsible for running and calculating the experiment. For other experiments, `Manager` need to rewrite some of the methods.
#### configs
The configuration part of the project. 

For convenience, I do not have a configuration method designed for serialization and deserialization. So some of the configurations need to be objects in Python. I declare all fields that need to be configured with `TypeDict`. 

All the prompt template are dynamically fetched, and modifying some of the templates can be done by modifying the kwargs of these methods. If no changes are made, these methods will generate the prompt template using default values.

For model client, I provide qwen series model. It is still possible to customize the corresponding factory methods to use other models.
#### prompts
All files related to prompts. I write a lot of prompt template, but end up using the methods in the `participant_prompts.py`. These methods encapsulate the tedious string handling, and modifying these templates is dynamic.
#### protocols
Protocols for the communication between agents. I define protocols using `dataclass` in Python. It would be more rigorous to use `pydantic`. But since this is a small system, it is easier to use `dataclass`. (In part because changes to the protocols are easier to modify.)
#### runtime
The runtime of autogen. I build a simple runner that encapsulates the operations of the runtime object.
#### subscriptions
The subscription mechanism is important for autogen. But here, for sake of simplicity, the way used is to call the agents directly. In the future, for more complex cases, it will be necessary to add some functional agents.
#### utils
The main problems is that some of the f-string operations are done at agent runtime, so I provide these two methods.
- Modify `{}` to make the f-string operation work.
- Convert JSON data to string. Put it into a markdown code block. Modify to make the f-string operation work.
### some demo
#### notebook demo
Some examples run with jupyter notebook. My notes from testing at the time.
#### result
An example of results saved from a single run an experiment. The save directory is customizable.

## Shortcoming
- Communication methods. I do not use the broadcast method because I need to make sure that the results are returned from each participant. This makes configuration a bit more difficult.
- The configuration is somewhat complex. I want to build the project to be reusable enough from the start. However, there are some parts that don't need to be that complex. Otherwise, the configuration module requires building an additional system.
- Logging. I implement my own logging and bind it to `manager`. However, `ClosureAgent` could be used here, or perhaps there are other better implementations.

## How to use
### 1. Perform the configuration
Set up the `_model_client.py`, `game_request.py`, `manager_config.py`, `participant_config.py` files in the `configs` package.
- `_model_client.py`  
  Other autogen supported model clients can be customized. Requires a custom factory method.
- `game_request.py`  
  Change the game settings. Mainly the number of round the experiment runs. It is also possible to massively change all relevant prompt templates.
- `manager_config.py`  
  Modify the game rule, the number of participants, the result storage path.
- `participant_config.py`  
  Change the underlying LLM of the participants, their identities, and the way they make inferences. 
Without modification, all settings will be configured as default. All `kwargs` that are set to `None` by default can be customized.
### 2. Run the experiment
Run `run_a_game.py`. You can see the output of the run process in the terminal. The results of the experiment are stored in the directory specified in the previous step.

## 

