# this allows to write handling logic that deals with the actual events including all fields rather than just a froamtted string.

# e.g: if you had defined this custom event and were emitting it. Then you could write the following handler to receive it.

import logging
from dataclasses import dataclass
from autogen_core import EVENT_LOGGER_NAME

@dataclass
class MyEvent:
    timestamp: str
    message: str

class MyHandler(logging.Handler):
    def __init__(self) ->None:
        super().__init__()

    def emit(self, record: logging.LogRecord) -> None:
        try:
            # use the structuredMessage if the message is an instance of it
            if isinstance(record.msg, MyEvent):
                print(f"Timestamp: {record.msg.timestamp}, Message: {record.msg.message}")
        except Exception:
            self.handleError(record)

logger = logging.getLogger(EVENT_LOGGER_NAME)
print(logger)
print(logger.setLevel(logging.INFO))
my_handler = MyHandler()
logger.handlers = [my_handler]     
print(logger.handlers)