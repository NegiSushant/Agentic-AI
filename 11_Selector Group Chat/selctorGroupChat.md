### SelectorGroupChat: implements a team where participants take turns broadcasting messages to all oter members. A generative model selects the next speaker based on the shared context, enabling dynamic, context-arware collaboration. Key features include:

* model-based speaker selection
* Configurable participant roles and descriptions
* Prevention of consecutive turns by the same speaker (optional)
* Customizable selection prompting
* Customizable selection function to override the default model-based selection

#### How does it Works? 

* it is a gruop chat similar to RundRobinGroupChat, but with a model-based next speaker selection mechanis. When the team receives a task through run() or run_stream(), the following steps are excuted:
  1. the team analyzes the current conversation context, including the conversation history and participants' name and description attributes, to determine the next speaker using a model. By default, the team will not select the same speak consecutively unless it is the only agent available. This can be changed by setting allow_repeated_speaker=Ture. You can also override the model by providing a custom selection function.
  2. the team prompts the selected speaker agent to provide a response, which is then broadcasted to all other participants.
  3. ther termination condition is checked to determine if the conversation should end, if not, the process repeats from step 1.
  4. When the conversation ends, the team returns the TaskResult containing the conversation history from this task.
* Once the team finished the task, the converstion context is kept within the team and all pariticipants, so the next task can continue from the previous conversation  context. we can reset the conversation context by calling reset().

# By default, [`AssistantAgent`](https://microsoft.github.io/autogen/stable/reference/python/autogen_agentchat.agents.html#autogen_agentchat.agents.AssistantAgent "autogen_agentchat.agents.AssistantAgent") returns the tool output as the response. If your tool does not return a well-formed string in natural language format, you may want to add a reflection step within the agent by setting `reflect_on_tool_use=True` when creating the agent. This will allow the agent to reflect on the tool output and provide a natural language response.
