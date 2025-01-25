# to implement this, set max_turns parameter in the RoundRobinGroupChat() constructor.
# e.g team = RoundRobinGroupChat([...], max_truns=1)

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from Client_initialization import client
# from ...Client_initialization import client
import asyncio


assitant = AssistantAgent(
    "assistant",
    model_client= client
)

team = RoundRobinGroupChat([assitant], max_turns=1)



async def main():
    task = input("Write task to your agent: ")
    while True:
        stream = team.run_stream(task = task)
        await Console(stream)
        # asyncio.run(Console(stream))
        task = input("Enter your feedback(type 'exit' to leave): ")
        # if 'exit' in task.lower():
        #     break
        if task.lower().strip() == 'exit':
            break

if __name__ == '__main__':
    asyncio.run(main())