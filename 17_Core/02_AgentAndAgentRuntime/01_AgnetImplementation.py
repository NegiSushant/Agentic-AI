from dataclasses import dataclass
from autogen_core import AgentId, MessageContext, RoutedAgent, message_handler, AgentRuntime
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
import asyncio
from autogen_core import SingleThreadedAgentRuntime
from dotenv import load_dotenv
import os

load_dotenv()
endpoint = os.getenv("AZURE_ENDPOINT")
Api_key = os.getenv("API_KEY")
apiVersion = os.getenv("OPENAI_API_VERSION")

client = AzureOpenAIChatCompletionClient(
    azure_depoyment_id="gpt-4o",
    model="gpt-4o",
    api_version= apiVersion,
    azure_endpoint=endpoint,
    api_key = Api_key,
)

@dataclass
class MyMessageType:
    content: str

class MyAgent(RoutedAgent):
    def __init__(self) -> None:
        super().__init__("MyAgent")

    @message_handler
    async def handle_my_message_type(self, message: MyMessageType, ctx: MessageContext) -> None:
        print(f"{self.id.type} received message: {message.content}")

#Wrapper agent for the AssistantAgent in AgentChat
class MyAssistant(RoutedAgent):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        model_client = client
        self._delegate = AssistantAgent(name, model_client=model_client)

    @message_handler
    async def handle_my_message_type(self, message: MyMessageType, ctx: MessageContext) -> None:
        print(f"{self.id.type} received message: {message.content}")
        response = await self._delegate.on_messages(
            [TextMessage(content=message.content, source="user")], ctx.cancellation_token
        )
        print(f"{self.id.type} responded: {response.chat_message.content}")

async def main():
    # agent = MyAgent()
    # message = await agent.handle_my_message_type(MyMessageType(message="hello! world,"), ctx=agent.id)

    runtime = SingleThreadedAgentRuntime()

    #register our agent types with the SingleThreadedAgentRuntime()
    await MyAgent.register(runtime, "my_agent", lambda: MyAgent())
    await MyAssistant.register(runtime, "my_assistant", lambda: MyAssistant("my_assistant"))

    # start processing messages in the background
    runtime.start()

    await runtime.send_message(MyMessageType("Hello, World!"), AgentId("my_agent", "default"))
    await runtime.send_message(MyMessageType("Hello, Negi!"), AgentId("my_assistant", "default"))
    await runtime.stop()
    # print(message)
    # async with SimpleAgentRuntime() as runtime:
    #     agent = await runtime.create_agent(MyAgent)

    #     # Simulate sending a message to the agent
    #     message = MyMessageType(content="Hello, Agent!")
    #     ctx = MessageContext(agent.id)

    #     await agent.handle_my_message_type(message, ctx)


if __name__ == "__main__":
    asyncio.run(main())