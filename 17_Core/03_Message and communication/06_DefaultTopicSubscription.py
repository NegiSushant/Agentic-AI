from autogen_core import MessageContext, RoutedAgent, TopicId, message_handler, type_subscription, TypeSubscription, DefaultTopicId, default_subscription
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


@default_subscription
class BroadcastingAgentDefaultTopic(RoutedAgent):
    @message_handler
    async def on_my_message(self, message: Message, ctx: MessageContext) -> None:
        #publish a message to all agents in the same namespace.
        await self.publish_message(
            Message("Publishing a message from broadcasting agent!"),
            topic_id=DefaultTopicId()
        )

runtime = SingleThreadedAgentRuntime()

async def main():
    await BroadcastingAgentDefaultTopic.register(
        runtime, "broadcasting_agent", lambda: BroadcastingAgentDefaultTopic("Broadcasting Agent")

    )
    await ReceivingAgent.register(runtime, "receiving_agent", lambda: ReceivingAgent("Receiving Agent"))

    runtime.start()
    await runtime.publish_message(Message("Hello world! from the runtime!"), topic_id=DefaultTopicId())
    await runtime.stop_when_idle()


if __name__ == "__main__":
    asyncio.run(main())