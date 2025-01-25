# when user or application intracts with the team of agents in an interactive loop like:
* the team runs until termination
* the application and user provides feedback
* team run again with the feedback

This approach is useful in a persisted session with asynchronous communication between the team and the application/user: Once a team finishes a run, the application saves the state of the team, puts it in a persistent storage, and resumes the team when the feedback arrives.


# There are two way to implement this approach:
* Set the maximum number of turns so that the team always stops after the specific number of turns.
* User termination conditions such as TextMentionTermination and HandoffTermination to allow the team to decide when to stop and give control back, given the team's internal state

## Using Max Turns
* This method allows you to pause the team for user input by setting a maximum number of turns.
* useful in scenarios where continuous user engagement is required, such as in a chatbot.

* To implement set the max_turns parameter in the RoundRobinGroupChat() constructor.

* e.g.: team = RoundRobinGroupChat([...], max_turns=1)
* Once the team stops, the turn count will be reset. When you resume the team, it will start from 0 again. However, the team’s internal state will be preserved.


# Using Termination Conditions
* HandoffTermination stops the team when an agent sends a HandoffMessage message

### The model used with AssistantAgent must support tool call to use the handoff feature.