##### Agent: 

* in AutoGen agent is an entity define by the base interface Agent.
* it has unique identifier of type AgentId, a metadata dictionary of the type AgentMetada.
* you can subclass your agents from higher level class [`RoutedAgent`](https://microsoft.github.io/autogen/stable/reference/python/autogen_core.html#autogen_core.RoutedAgent "autogen_core.RoutedAgent") which enables you to route messages to corresponding message handler specified with [`message_handler()`](https://microsoft.github.io/autogen/stable/reference/python/autogen_core.html#autogen_core.message_handler "autogen_core.message_handler") decorator and proper type hint for the `message` variable. An agent runtime is the execution environment for agents in AutoGen.

**For local development, developers can use [`SingleThreadedAgentRuntime`](https://microsoft.github.io/autogen/stable/reference/python/autogen_core.html#autogen_core.SingleThreadedAgentRuntime "autogen_core.SingleThreadedAgentRuntime")**

### Agent Implementation:

* must subclass the RoutedAgent class
* implement a message handler method for each message type the agent is expected to handle using the message_handler())
