#  create a simple agent that counts down from a given number to zero, and produces a stream of messages with the current count.

from typing import AsyncGenerator, List, Sequence, Tuple

from autogen_agentchat.agents import BaseChatAgent
from autogen_agentchat.base import Response
from autogen_agentchat.messages import AgentEvent, ChatMessage, TextMessage
from autogen_core import CancellationToken
import asyncio


class CountDownAgent(BaseChatAgent):
    def __init__(self, name: str, count: int = 3):
        super().__init__(name, "Count Down Agent")
        self._count = count

    
    @property
    def produced_message_types(self)->Sequence[type[ChatMessage]]:
        return (TextMessage)
    
    async def on_messages(self, messages: Sequence[ChatMessage], cancellation_token: CancellationToken) -> Response:
        #Calls the on_messages_stream
        response: Response | None = None
        
        async for message in self.on_messages_stream(messages, cancellation_token):
            if isinstance(message, Response):
                response = message
        assert response is not None
        return response
    

    async def on_messages_stream(self, messages:Sequence[ChatMessage], cancellation_token: CancellationToken)-> AsyncGenerator[AgentEvent | ChatMessage | Response, None]:
        inner_messages: List[AgentEvent | ChatMessage] = []
        for i in range(self._count, 0, -1):
            msg = TextMessage(content=f"{i}...", source= self.name)
            inner_messages.append(msg)
            yield msg
        
        #the response is returned at the end of the stream
        # It contains the final message and the inner messages.
        yield Response(chat_message=TextMessage(content="Done!", source=self.name), inner_messages=inner_messages)
    
    async def on_reset(self, cancellation_token:CancellationToken)-> None:
        pass

async def run_countdown_agent()-> None:
    #create a countdown agent
    agent = CountDownAgent("countdown")

    #run the agent with a give task and steam the response
    async for message in agent.on_messages_stream([], CancellationToken()):
        if isinstance(message, Response):
            print(message.chat_message.content)
        else:
            print(message.content)


asyncio.run(run_countdown_agent()) 