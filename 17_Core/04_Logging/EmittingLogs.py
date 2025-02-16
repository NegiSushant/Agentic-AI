# These two names are the root loggers for these types. Code that emits logs should use a child logger of these loggers. For example, if you are writing a module my_module and you want to emit trace logs, you should use the logger named:
import logging

from autogen_core import TRACE_LOGGER_NAME
logger = logging.getLogger(f"{TRACE_LOGGER_NAME}.my_module")

print(logger)

import logging
from dataclasses import dataclass
from autogen_core import EVENT_LOGGER_NAME

@dataclass
class MyEvent:
    timestamp: str
    message: str

logger = logging.getLogger(EVENT_LOGGER_NAME + ".my_module")
logger.info(MyEvent("timestamp", "message"))