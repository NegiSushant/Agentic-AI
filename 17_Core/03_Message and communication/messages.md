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

