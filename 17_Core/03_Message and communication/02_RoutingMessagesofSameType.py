from autogen_core import AgentId, MessageContext, RoutedAgent,  SingleThreadedAgentRuntime, message_handler
# from autogen_agentchat.messages import TextMessage
import asyncio
from dataclasses import dataclass


@dataclass
class TextMessage:
    content: str
    source: str

@dataclass
class ImageMessage:
    url: str
    source : str


class RoutedBySenderAgent(RoutedAgent):
    @message_handler(match=lambda msg, ctx: msg.source.startswith("user1")) # type: ignor
    async def on_user1_message(self, message: TextMessage, ctx: MessageContext)-> None:
        print(f"Hello from user 1 handler, {message.source}, you said {message.content}!")

    @message_handler(match=lambda msg, ctx: msg.source.startswith("user2"))
    async def on_user2_message(self, message: TextMessage, ctx: MessageContext) -> None:
        print(f"Hello from user 2 handler, {message.source}, you said {message.content}!")

    @message_handler(match=lambda msg, ctx: msg.source.startswith("user2"))
    async def on_image_message(self, message: ImageMessage, ctx: MessageContext) -> None:
        print(f"Hello, {message.source}, you sent me {message.url}!")

runtime = SingleThreadedAgentRuntime()

async def main():
    start = await RoutedBySenderAgent.register(runtime, "my_agent", lambda: RoutedBySenderAgent("Routed by sender agent"))
    print(f"start: {start}")
    runtime.start()
    agent_id = AgentId("my_agent", "default")
    await runtime.send_message(TextMessage(content="Hello, India!", source = "user1- test"), agent_id)
    await runtime.send_message(TextMessage(content="Hello, Bharat!", source = "user2- test"), agent_id)
    await runtime.send_message(ImageMessage(url="https://something.com/image.jpg", source="user1-test"), agent_id)
    await runtime.send_message(ImageMessage(url="https://something.com/image.jpg", source="user2-test"), agent_id)


if __name__ == "__main__":
    asyncio.run(main())