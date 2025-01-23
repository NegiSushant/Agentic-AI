import os
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import TaskResult
from autogen_agentchat.conditions import ExternalTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_core import CancellationToken
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from dotenv import load_dotenv


load_dotenv()
endpoint = os.getenv("AZURE_ENDPOINT")
Api_key = os.getenv("API_KEY")
apiVersion = os.getenv("OPENAI_API_VERSION")



client = AzureOpenAIChatCompletionClient(
    azure_depoyment_id="gpt-4o",
    model="gpt-4o",
    api_version= apiVersion,
    azure_endpoint=endpoint,
    # AZURE_OPENAI_API_KEY = Api_key
    api_key = Api_key,
)


primary_agent = AssistantAgent(
    name="primary",
    model_client=client,
    system_message="You are a helpful AI assistant."
)


critic_agent = AssistantAgent(
    name="critic",
    model_client=client,
    system_message="Provide constructive feedback. Respond with 'APPROVE' to when your feedbacks are addressed."
)
text_termination = TextMentionTermination("APPROVE")

external_termination = ExternalTermination()
team = RoundRobinGroupChat([primary_agent, critic_agent], termination_condition= external_termination | text_termination)


async def StopAgent():
    #run the team in a background task
    # run = asyncio.create_task(Console((team.run_stream(task="Write a short poem about the fall season.")))
    run = await (team.run(task="Write a short poem about the fall season."))
    await asyncio.sleep(0.1)
    external_termination.set()
    team.run_stream() #resume a team to continue from where it left off by calling the run() or run_stream() method again without a new task.
    return run



async def main():
    result = await StopAgent()
    print(result)


if __name__ == "__main__":
    asyncio.run(main())