### Swarm implements a team in which agents can hand off task to other agents based on their capabilities. It is a multi-agent design pattern first introduced by OpenAI in Swarm.

- **"key ides is to let agent delegate tasks to other agents using a special tool call, while all agents share the same message context. this enables agents to make local decisions about task planning, rather than replying on central orchesrator such as in SelectorGroupChat."**

##### How Does it Work?

- Swarm team is group chat where agents take turn to generate a response. Similar to SelectorGroupChat and RoundRoubinGroupChat participants agents broadcast their responses to all agents share the same message context.
- at each turn, the speaker agent is selected based on the most recent HandOffMessage message in the context. This naturally requires each agent in the team to be able to generate HandoffMessage to signal which other agents that it hands off to.
- For [`AssistantAgent`](https://microsoft.github.io/autogen/stable/reference/python/autogen_agentchat.agents.html#autogen_agentchat.agents.AssistantAgent "autogen_agentchat.agents.AssistantAgent"), you can set the `handoffs` argument to specify which agents it can hand off to. You can use [`Handoff`](https://microsoft.github.io/autogen/stable/reference/python/autogen_agentchat.base.html#autogen_agentchat.base.Handoff "autogen_agentchat.base.Handoff") to customize the message content and handoff behavior.
- overall process can be summarized as follows:
  1. Each agent has the ability to generate HandoffMessage to singnal which other agents it can hanfd off to. For AssistantAgent, this means setting the handoffs argument.
  2. when team starts on a task, the first speaker agents operate on the task and make locallized decision about whether to hand off and to whom.
  3. When agent generates a HandoffMessage, the receiving agent takes over the task with the same message context.
  4. the process continues until a termination condition is met.

#### The [`AssistantAgent`](https://microsoft.github.io/autogen/stable/reference/python/autogen_agentchat.agents.html#autogen_agentchat.agents.AssistantAgent "autogen_agentchat.agents.AssistantAgent") uses the tool calling capability of the model to generate handoffs. This means that the model must support tool calling. If the model does parallel tool calling, multiple handoffs may be generated at the same time. This can lead to unexpected behavior. To avoid this, you can disable parallel tool calling by configuring the model client. For [`OpenAIChatCompletionClient`](https://microsoft.github.io/autogen/stable/reference/python/autogen_ext.models.openai.html#autogen_ext.models.openai.OpenAIChatCompletionClient "autogen_ext.models.openai.OpenAIChatCompletionClient") and [`AzureOpenAIChatCompletionClient`](https://microsoft.github.io/autogen/stable/reference/python/autogen_ext.models.openai.html#autogen_ext.models.openai.AzureOpenAIChatCompletionClient "autogen_ext.models.openai.AzureOpenAIChatCompletionClient") you can set `parallel_tool_calls=False` in the configuration.
