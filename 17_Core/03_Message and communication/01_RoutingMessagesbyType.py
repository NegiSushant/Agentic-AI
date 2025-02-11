from autogen_core import AgentId, MessageContext, RoutedAgent,  SingleThreadedAgentRuntime, message_handler
# from autogen_agentchat.messages import TextMessage
import asyncio
from dataclasses import dataclass


@dataclass
class TextMessage:
    content: str

@dataclass
class ImageMessage:
    content: str

class MyAgent(RoutedAgent):
    @message_handler
    async def on_text_message(self, message: TextMessage, ctx: MessageContext) -> None:
        print(f"Hello, {message.source}, you said {message.content}!")
    
    @message_handler
    async def on_image_message(self, message: ImageMessage, ctx: MessageContext) -> None:
        print(f"Hello, {message.source}, you sent me {message.url}!")

async def main():
    runtime = SingleThreadedAgentRuntime()
    await MyAgent.register(runtime, "my_agent", lambda: MyAgent("My Agent"))
    # AgentType(type='my_agent')

    runtime.start()
    agent_id = AgentId("my_agent", "default")
    await runtime.send_message(TextMessage(content="Hello, World!", source="User"), agent_id)
    await runtime.send_message(ImageMessage(url="https://example.com/image.jpg", source="User"), agent_id)
    await runtime.stop_when_idle()


if __name__ == "__main__":
    asyncio.run(main())