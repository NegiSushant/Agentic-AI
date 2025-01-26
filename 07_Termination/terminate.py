from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from Client_initialization import client
import asyncio


agent1 = AssistantAgent(
    "primary_agent",
    model_client= client,
    system_message="You are a helpful AI assistant"
)

agent2 = AssistantAgent(
    "critic_agent",
    model_client=client,
    system_message="Provide constructive feedback for every message. Respond with 'APPROVE' to when your feedbacks are addressed."
)

max_msg_terminate = MaxMessageTermination(max_messages=10)
text_terminate = TextMentionTermination("APPROVE")
# combined_terminate = max_msg_terminate | text_terminate
combined_terminate = max_msg_terminate & text_terminate


team = RoundRobinGroupChat([agent1,agent2], termination_condition=max_msg_terminate)

async def main():
    task = input("give the task to the agents: ")
    await Console(team.run_stream(task=task)) 

if __name__ == "__main__":
    asyncio.run(main())