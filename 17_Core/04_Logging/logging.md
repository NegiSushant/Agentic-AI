there are 2 kinds of logging:
* Trace Logging: used to debugging and human readable messages to indicate what is going on. content and format of these logs should not be depended on by other system.
        Name: TRACE_LOGGER_NAME
* Structured logging: this logger emits structured events that can be consumed by other system. content and format of these logs can be depended on by other systems.
        Name: EVENT_LOGGER_NAME.
    
* ROOT_LOGGER_NAME can be used to enable or disable all logs.

#### Enabling logging output
To enable trace logging, you can use the following code:

import logging

from autogen_core import TRACE_LOGGER_NAME

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(TRACE_LOGGER_NAME)
logger.setLevel(logging.DEBUG)