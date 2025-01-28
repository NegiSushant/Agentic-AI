from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken
from Client_initialization import client
import asyncio
import json

agent1 = AssistantAgent(
    name="assistant_agent",
    system_message="You are a helpful assistant",
    model_client=client
)

team = RoundRobinGroupChat([agent1], termination_condition=MaxMessageTermination(max_messages=2))

async def main():
    #Run the team and stream messages to the console
    stream = team.run_stream(task="Write a beautiful poem 3 -line about dul lake.")
    res = await Console(stream)
    team_state = await team.save_state()

    ##save state to disk 
    with open("team_state.json", "w") as f:
        json.dump(team_state, f)
    
    #load state from disk
    with open("team_state.json", "r") as f:
        team_state = json.load(f)
    
    new_agent_team = RoundRobinGroupChat([agent1], termination_condition=MaxMessageTermination(max_messages=2))
    await new_agent_team.load_state(team_state)
    stream = new_agent_team.run_stream(task="What was the last line of the poem you wrote?")
    await Console(stream)

if __name__ == "__main__":
    asyncio.run(main())