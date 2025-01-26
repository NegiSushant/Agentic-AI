### AgentChat supports several termination condition by providing a base TerminationCondition class and several implementations that inherit from it.

A termination condition is a callable that takes a sequence of AgentEvent or ChatMessage objects since the last time the condition was called and returns a termination condition has been reached, it must be reset by calling reset() before it can be used again.

## note about termination conditions:

- They are stateful but reset automatically after each run(run()) or run_stream() is finished.
- can be combined using the AND(&) and OR(|) operator.

# Built-In termination Conditions:

- MaxMessageTermination: stops after number of messages heve been produced by both agent and task messages. e.g. MaxMessageTermination(max_messages = 4)
- TextMentionTermination: stop when specific text or string is mentioned in a message. (e.g. "TERMINATE" or "STOP" or "EXIT")
- TokenUsageTermination: stops when certain number of Tokens(prompt or completion) are used. this requires the agents to report token usage in their messages.
- TimeoutTermination: Stops after a specified duration in seconds.
- HandoffTermination: Stops when a handoff to a specific target is requested. Handoff messages can be used to build patterns such as Swarm. This is useful when you want to pause the run and allow application or user to provide input when an agent hands off to them.
- SourceMatchTermination: stops after specifc agent responds.
- ExternalTermination: Enables programmatic control of termination from outside the run. useful for UI integration(e.g. stop or exit button in chat interface.)
- StopMessageTermination: Stops when a stopMessage is produced by an agent.
