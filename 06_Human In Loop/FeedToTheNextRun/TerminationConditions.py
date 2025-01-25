import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import Handoff, TaskResult
from autogen_agentchat.conditions import HandoffTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from Client_initialization import client

lazy_agent = AssistantAgent(
    "lazy_assistant",
    model_client= client,
    handoffs=[Handoff(target="user",message="Transfer to user.")],
    system_message = "Always transfer to user when you don't know the answer. Respond 'TERMINATE' when task is complete."
)

# Define a termination condition that checks for handoff message targetting helper and text "TERMINATE".
handoff_termination = HandoffTermination(target="user")
text_termination = TextMentionTermination("TERMINATE")
combined_termination = handoff_termination | text_termination


#creating a single-agent team
lazy_agent_team = RoundRobinGroupChat([lazy_agent], termination_condition=combined_termination)

async def call_result(task):
    result = lazy_agent_team.run_stream(task=task)
    
    print(result)


async def main():
    task = input("make ask for your agent: ")
    # async for message in lazy_agent_team.run_stream(task=task):
    #     if isinstance(message, TaskResult):
    #         print("Stop Reason:", message.stop_reason)
    #     else: 
    #         print(message)
    result = await call_result(task)
    print(result)

if __name__ == '__main__':
    asyncio.run(main())