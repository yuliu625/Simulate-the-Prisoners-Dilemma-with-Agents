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
- `participant` is a good enough implementation that this agent can simulate many participants of multiple experiments.
- `manager` is the manager of the experiment and is responsible for running and calculating the experiment. For other experiments, `manager` need to rewrite some of the methods.
#### configs
The configuration part of the project. 

For convenience, I do not have a configuration method designed for serialization and deserialization. So some of the configurations need to be objects in Python. I declare all fields that need to be configured with `TypeDict`. 

All the prompt template are dynamically fetched, and modifying some of the templates can be done by modifying the kwargs of these methods. If no changes are made, these methods will generate the prompt template using default values.

For model client, I provide qwen series model. It is still possible to customize the corresponding factory methods to use other models.

### some demo
#### notebook demo

#### result


## Shortcoming


## How to use


## 

