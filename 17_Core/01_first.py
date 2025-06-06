from dataclasses import dataclass
from typing import Callable
from autogen_core import DefaultTopicId, MessageContext, RoutedAgent, default_subscription, message_handler
from autogen_core import AgentId, SingleThreadedAgentRuntime
import asyncio


@dataclass
class Message:
    content: int

@default_subscription
class Modifier(RoutedAgent):
    def __init__(self, modify_val: Callable[[int], int])-> None:
        super().__init__("A modifier agent.")
        self._modify_val = modify_val

    @message_handler
    async def handle_message(self, message: Message, ctx: MessageContext)-> None:
        val = self._modify_val(message.content)
        print(f"{'-'*80}\nModifier:\Modified {message.content} to {val}")
        await self.publish_message(Message(content=val), DefaultTopicId())

@default_subscription
class Checker(RoutedAgent):
    def __init__(self, run_until: Callable[[int], bool]) -> None:
        super().__init__("A Checker agent.")
        self._run_until = run_until

        @message_handler
        async def handle_message(self, message: Message, ctx: MessageContext) -> None:
            if not self._run_until(message.content):
                print(f"{'-'*80}\nChecker:\n{message.content} passed the check, continue.")
                await self.publish_message(Message(content=message.content), DefaultTopicId())
            else:
                print(f"{'-'*80}\nChecker:\n{message.content} failed the check, stopping.")
    

#create an local embedded runtime for agent.
runtime = SingleThreadedAgentRuntime()

#register the modifier and checker agents by providing their agent types, the factory functions for creating instance and subscriptions.
async def Agents():
    await Modifier.register(
        runtime,
        "modifier",
        lambda: Modifier(modify_val=lambda x: x-1)

    )
    await Checker.register(
        runtime,
        "checker",
        lambda: Checker(run_until=lambda x: x<=1)
    )

    runtime.start()
    await runtime.send_message(Message(10), AgentId("checker","default"))
    await runtime.stop_when_idle()

async def main():
    await Agents()

    
if __name__ =="__main__":
    asyncio.run(main())
