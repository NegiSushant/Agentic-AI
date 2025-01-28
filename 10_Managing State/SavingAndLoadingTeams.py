from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken
from Client_initialization import client
import asyncio

agent0 = AssistantAgent(
    name="assistant_agent",
    system_message="You are a helpful assistant",
    model_client=client
)

team = RoundRobinGroupChat([agent0], termination_condition=MaxMessageTermination(max_messages=2))

async def main():
    #Run the team and stream messages to the console
    stream = team.run_stream(task="Write a beautiful poem 3 -line about dul lake.")
    res = await Console(stream)
    team_state = await team.save_state()
    # if we reset the team (simulating instantiation of the team), and ask the question, team is unable to accomplish there.
    await team.reset()
    stm = team.run_stream(task="What was the last line of the poem you wrote?")
    await Console(stm)
    print(team_state)

    # load the state of the team and ask the same question. and team is able to accurately return the last line of the poem it wrote.
    await team.load_state(team_state)
    st1 = team.run_stream(task="What is the last line of the poem you wrote?")
    await Console(st1)

if __name__ == "__main__":
    asyncio.run(main())