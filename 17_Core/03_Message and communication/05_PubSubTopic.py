from autogen_core import MessageContext, RoutedAgent, TopicId, message_handler, type_subscription, TypeSubscription
from dataclasses import dataclass
from autogen_core import SingleThreadedAgentRuntime
import asyncio


@dataclass
class Message:
    content: str

@type_subscription(topic_type="default")
class ReceivingAgent(RoutedAgent):
    @message_handler
    async def on_my_message(self, message: Message, ctx: MessageContext)-> None:
        print(f"Received a message: {message.content}")

class BroadcastingAgent(RoutedAgent):
    @message_handler
    async def on_my_messages(self, message: Message, ctx: MessageContext) -> None:
        await self.publish_message(
            MessageContext("Publishing a message from broadcating agent!"),
            topic_id=TopicId(type="default", source=self.id.key)
        )

runtime = SingleThreadedAgentRuntime()

async def main():
    # Option 1: with type_subscription decorator
    # The type_subscription class decorator automatically adds a TypeSubscription to
    # the runtime when the agent is registered.
    res1 = await ReceivingAgent.register(runtime, "receiving_agent", lambda: ReceivingAgent("Receiving Agent"))
    print(f"option1: {res1}")
    
if __name__ == "__main__":
    asyncio.run(main())