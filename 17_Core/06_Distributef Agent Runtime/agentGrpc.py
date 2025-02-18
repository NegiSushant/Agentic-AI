from dataclasses import dataclass
from autogen_core import DefaultTopicId, MessageContext, RoutedAgent, default_subscription, message_handler
from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntime
from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntimeHost
import asyncio

@dataclass
class MyMessage:
    content: str

@default_subscription
class MyAgent(RoutedAgent):
    def __init__(self, name: str) -> None:
        super().__init__("My agent")
        self._name = name
        self._counter = 0

    @message_handler
    async def my_message_handler(self, message: MyMessage, ctx: MessageContext) -> None:
        self._counter += 1
        if self._counter > 5:
            return
        content = f"{self._name}: Hello x {self._counter}"
        print(content)
        await self.publish_message(MyMessage(content=content), DefaultTopicId())

# host = GrpcWorkerAgentRuntimeHost(address="localhost:50051")
# host.start()

# worker1 = GrpcWorkerAgentRuntime(host_address="localhost:50051")
# worker2 = GrpcWorkerAgentRuntime(host_address="localhost:50051")

async def main():
    host = GrpcWorkerAgentRuntimeHost(address="localhost:50051")
    host.start()

    worker1 = GrpcWorkerAgentRuntime(host_address="localhost:50051")
    await worker1.start()
    await MyAgent.register(worker1, "worker1", lambda: MyAgent("worker1"))

    worker2 = GrpcWorkerAgentRuntime(host_address="localhost:50051")
    await worker2.start()
    await MyAgent.register(worker2, "worker2", lambda: MyAgent("worker2"))

    await worker2.publish_message(MyMessage(content="Hello!"), DefaultTopicId())

    # Let the agents run for a while.
    await asyncio.sleep(5)
    await worker1.stop()
    await worker2.stop()

    # To keep the worker running until a termination signal is received (e.g., SIGTERM).
    # await worker1.stop_when_signal()

    await host.stop()

    # To keep the host service running until a termination signal (e.g., SIGTERM)
    # await host.stop_when_signal()

if __name__ == "__main__":
    asyncio.run(main())
