from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken
from Client_initialization import client
import asyncio


assistant_agent = AssistantAgent(
    name="assistant_agent",
    system_message="You are a helppful assistant",
    model_client=client,
)

agent1 = AssistantAgent(
    name="agent1",
    system_message="You are a helpful assistant",
    model_client=client
)


async def agent0Call():
    response = await assistant_agent.on_messages(
        [TextMessage(content="Write a 3 line poem on lake tangayika", source="user")], CancellationToken()
    )
    print(response.chat_message.content)
    agent_state = await assistant_agent.save_state()
    print(agent_state)
    res = await agent1.load_state(agent_state)

    res1 = await agent1.on_messages(
        [TextMessage(content="What was the last line of the previous poem you wrote", source='user')], CancellationToken()
    )

    print(res1.chat_message.content)

# async def agent1Call():
#     res = await agent1.load_state
async def main():
    await agent0Call()

if __name__ == "__main__":
    asyncio.run(main())