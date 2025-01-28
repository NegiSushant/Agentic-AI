from typing import Callable, Sequence, List
import asyncio
from autogen_agentchat.agents import BaseChatAgent
from autogen_agentchat.base import Response
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.messages import ChatMessage, TextMessage
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken
from Client_initialization import client


class ArithmeticAgent(BaseChatAgent):
    def __intit__(self, name: str, description: str, operator_func: Callable[[int], int]) -> None:
        super().__init__(name, description=description)
        self._operator_func = operator_func
        self._message_history: List[ChatMessage] = []

    @property
    def produced_message_types(self) -> Sequence[type[ChatMessage]]:
        return (TextMessage,)
    
    async def on_messages(self, messages: Sequence[ChatMessage], cancellation_token: CancellationToken)-> Response:
        #update the message history.
        #Note: it is possible the messages is empty list, which means the agent was selected previously.
        self._message_history.extend(messages)
        #parse the number in the last message
        assert isinstance(self._message_history[-1], TextMessage)
        number = int(self._message_history[-1].content)

        #Apply the operator function to the number
        result = self._operator_func(number)
        #create a new message with the result
        response_message = TextMessage(content= str(result), source=self.name)
        #Update the message hitory
        self._message_history.append(response_message)
        
        #return the response
        return Response(chat_message=response_message)

    async def on_reset(self, cancellation_token: CancellationToken) -> None:
        pass


async def run_number_agents() -> None:
    #create agents for number operations
    add_agent = ArithmeticAgent("add_agent", "Adds 1 to the number.", lambda x: x+1)
    multiply_agent = ArithmeticAgent("multiply_agent", "Multiplies the number by 2.", lambda x: x*2)
    subtract_agent = ArithmeticAgent("substract_anget", "Subtracts 1 from the number.", lambda x: x-1)
    divide_agent = ArithmeticAgent("divide_agent", "Divides the number by 2 and rounds down.", lambda x: x // 2)
    identity_agent = ArithmeticAgent("identity_agent", "Return the numeber as is.", lambda x: x)


    #The termination condition is to stop after 10 message
    termination_condition = MaxMessageTermination(10)

    #Create a selector group chat
    selector_group_chat = SelectorGroupChat(
        [add_agent, multiply_agent, subtract_agent, divide_agent, identity_agent],
        model_client= client,
        termination_condition=termination_condition,
        allow_repeated_speaker=True, #ALlow the same agent to speak multiple times, necessary for this task.
        selector_prompt=(
            "Available roles: \n{roles}\nTheir job descriptions:\n{participants}\n"
            "Current conversation history: \n{history}\n"
            "Please select the most appropriate role for the next message, and only return the role name."
        )
    )

    # Run the selector group chat with a given task and stream the response.
    task: List[ChatMessage] = [
        TextMessage(content= "Apply the operations to turn the given number into 25.", source="user"),
        TextMessage(content="10", source="user")
    ]

    stream = selector_group_chat.run_stream(task=task)
    await Console(stream)


async def main():
    result = await run_number_agents()

if __name__ == "__main__":
    asyncio.run(main())