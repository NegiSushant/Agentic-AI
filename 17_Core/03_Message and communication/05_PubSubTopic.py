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

    #option 2: with TypeSubscription
    res2 = await BroadcastingAgent.register(runtime, "broadcasting_agent", lambda: BroadcastingAgent("Broadcasting Agent"))
    print(f"option2 res2: {res2}")
    res21 = await runtime.add_subscription(TypeSubscription(topic_type="default", agent_type="broadcasting_agent"))
    print(f"option2 res21: {res21}")

    #start the runtime and publish a message.
    runtime.start()
    final_res = await runtime.publish_message(
        Message("Hello, World! From the runtime!"),
        topic_id=TopicId(type="default", source="default")
    )
    print(f"Final res:{final_res}")
    await runtime.stop_when_idle()
    
if __name__ == "__main__":
    asyncio.run(main())