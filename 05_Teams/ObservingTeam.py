import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import TaskResult
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import ExternalTermination, TextMentionTermination
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken
from dotenv import load_dotenv
from autogen_core.model_context import BufferedChatCompletionContext
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
import os

load_dotenv()
endpoint = os.getenv("AZURE_ENDPOINT")
Api_key = os.getenv("API_KEY")
apiVersion = os.getenv("OPENAI_API_VERSION")

#create the token provider
# token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")


client = AzureOpenAIChatCompletionClient(
    azure_depoyment_id="gpt-4o",
    model="gpt-4o",
    api_version= apiVersion,
    azure_endpoint=endpoint,
    # AZURE_OPENAI_API_KEY = Api_key
    api_key = Api_key,
    # agent that uses only the last 5 messages in the context to generate responses. for more info see the 04_ModelContext.py
    model_context=BufferedChatCompletionContext(buffer_size=5),
)

primary_client = AssistantAgent(
    name="primary",
    model_client= client,
    system_message="You are a helpfull AI assistant."
)

critic_agent = AssistantAgent(
    name="critic",
    model_client= client,
    system_message="Provide constructive feedback. Respond with 'APPROVE' to when your feedbacks are addressed."
)

#Define a termination condition that stops the task if the critics approves.
text_termination = TextMentionTermination("APPROVE")

#creating a team with the primary and critic agent
team = RoundRobinGroupChat(
    [primary_client, critic_agent],
    termination_condition= text_termination
)

async def main():
    
    async for message in team.run_stream(task="Write a short poem about the winter season."):
        if isinstance(message, TaskResult):
            print("Stop Reason:", message.stop_reason)
        else: 
            print(message)
    await team.reset() #this mathod clear the team status, including all agents. It will call the each agent's on_reset() method to clear the agent's state
    # result = await team.run(task="Write a short poem about the winter season.")
    # print(result)
    return

if __name__ == "__main__":
    asyncio.run(main())
