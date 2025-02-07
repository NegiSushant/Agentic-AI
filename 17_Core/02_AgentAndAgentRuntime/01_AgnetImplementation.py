from dataclasses import dataclass
from autogen_core import AgentId, MessageContext, RoutedAgent, message_handler, AgentRuntime
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import asyncio
from autogen_core import SingleThreadedAgentRuntime


@dataclass
class MyMessageType:
    content: str

class MyAgent(RoutedAgent):
    def __init__(self) -> None:
        super().__init__("MyAgent")

    @message_handler
    async def handle_my_message_type(self, message: MyMessageType, ctx: MessageContext) -> None:
        print(f"{self.id.type} received message: {message.content}")


class MyAssistant(RoutedAgent):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o")
        self._delegate = AssistantAgent(name, model_client=model_client)

    @message_handler
    async def handle_my_message_type(self, message: MyMessageType, ctx: MessageContext) -> None:
        print(f"{self.id.type} received message: {message.content}")
        response = await self._delegate.on_messages(
            [TextMessage(content=message.content, source="user")], ctx.cancellation_token
        )
        print(f"{self.id.type} responded: {response.chat_message.content}")

async def main():
    agent = MyAgent()
    message = await agent.handle_my_message_type(MyMessageType(message="hello! world,"), ctx=agent.id)

    print(message)
    # async with SimpleAgentRuntime() as runtime:
    #     agent = await runtime.create_agent(MyAgent)

    #     # Simulate sending a message to the agent
    #     message = MyMessageType(content="Hello, Agent!")
    #     ctx = MessageContext(agent.id)

    #     await agent.handle_my_message_type(message, ctx)


if __name__ == "__main__":
    asyncio.run(main())