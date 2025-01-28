Managing State is useful in a web application where stateless endpoints respond to requests and need to load the state of the application from persistent storage.

## Saving and Loading Agents

* We can get the state of an agent by calling save_state() method on an AssistantAgent

##### ***For [`<span class="pre">AssistantAgent</span>`](https://microsoft.github.io/autogen/stable/reference/python/autogen_agentchat.agents.html#autogen_agentchat.agents.AssistantAgent "autogen_agentchat.agents.AssistantAgent"), its state consists of the model_context. If your write your own custom agent, consider overriding the [`<span class="pre">save_state()</span>`](https://microsoft.github.io/autogen/stable/reference/python/autogen_agentchat.agents.html#autogen_agentchat.agents.BaseChatAgent.save_state "autogen_agentchat.agents.BaseChatAgent.save_state") and [`<span class="pre">load_state()</span>`](https://microsoft.github.io/autogen/stable/reference/python/autogen_agentchat.agents.html#autogen_agentchat.agents.BaseChatAgent.load_state "autogen_agentchat.agents.BaseChatAgent.load_state") methods to customize the behavior. The default implementations save and load an empty state.***

## Saving and Loading Teams

* We can get the state of team by calling save_state method on the team and load it back by calling load_state method on the team
* When we call save_state on team, it saves the state of all the agents in the team.
* we will begin by creating a simple RoundRobinGroupChat team with a single agent and ask it to write a poem.
