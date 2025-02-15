An agent in AutoGen core can react to, send and publish messages and messages are the only means through which agents can communicate with each other.

### Messages are serializable objects, they can defined using:

- A subclass of Pydantic's pydantic.BaseModel
- A dataclass

e.g.
from dataclasses import dataclass

@dataclass
class TextMessage:
content: str
source: str

@dataclass
class ImageMessage:
url: str
source: str

# Messages are purely data, and should not contain any logic.

# Message Handlers:

- when agent recevies a message the runtime will invoke the agent's message handler (on_message()) which should implement the agents message handling logic.
- if message cannot be handled by agent, the agent should raise a CantHandleException.
- BaseAgent (base class) does not provide message handling logic and implementing the on_message() method directly is not recommended unless for the advanced use cases.
- implement the RoutedAgent base class which provides built-in message routing capability.

# Routing messages by Type

- the RoutedAgnet base class provides a mechanism for associating message types with message handlers with the message_handler() decorator, so do not need to implement the on_message() method.

# Routing Messages of the Same Type

- useful to route messages of the same type to different handlers. e.g. message from different sender agents should be handled differently.
- use the match parameter of the message_handler() decorator.
- match parameter associates handlers for the same message type to a specific message, which is secondary to the message type routing, accepts a callable that takes the message and MessageContext as arguments, return boolean which indicate wether the message should be handled by the decorated handler.

# Direct Messaging

- two types of communication in AutoGen core:
  - **Direct Messaging:** sends a direct message to another agent.
    - to send a direct message to another agent, within a message handler use the [`autogen_core.BaseAgent.send_message()`](https://microsoft.github.io/autogen/stable//reference/python/autogen_core.html#autogen_core.BaseAgent.send_message "autogen_core.BaseAgent.send_message")method, from the runtime use the [`autogen_core.AgentRuntime.send_message()`](https://microsoft.github.io/autogen/stable//reference/python/autogen_core.html#autogen_core.AgentRuntime.send_message "autogen_core.AgentRuntime.send_message") method. Awaiting calls to these methods will return the return value of the receiving agent’s message handler. When the receiving agent’s handler returns `None`, `None` will be returned.
    - **_If the invoked agent raises an exception while the sender is awaiting, the exception will be propagated back to the sender._**
    - Direct messaging can be used for request/response scenarios, where the sender expects a response from the receiver. The receiver can respond to the message by returning a value from its message handler. You can think of this as a function call between agents.
  - **Broadcast:** publishes a message to a topic.
  - Broadcast is effectively the pub/sub model with topic and subscription.
  - the key difference between direct messaging and broadcast is that broadcast cannot be used for request/response scenarios. when an agent publishs a message it is one way only, it can't receive response from any other agent, even if a receiving agent's handler return a value.
