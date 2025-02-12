An agent in AutoGen core can react to, send and publish messages and messages are the only means through which agents can communicate with each other.

### Messages are serializable objects, they can defined using:

* A subclass of Pydantic's pydantic.BaseModel
* A dataclass

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

* when agent recevies a message the runtime will invoke the agent's message handler (on_message()) which should implement the agents message handling logic.
* if message cannot be handled by agent, the agent should raise a CantHandleException.
* BaseAgent (base class) does not provide message handling logic and implementing the on_message() method directly is not recommended unless for the advanced use cases.
* implement the RoutedAgent base class which provides built-in message routing capability.

# Routing messages by Type

* the RoutedAgnet base class provides a mechanism for associating message types with message handlers with the message_handler() decorator, so do not need to implement the on_message() method.
*
