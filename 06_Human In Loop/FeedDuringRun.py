from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
import os
from dotenv import load_dotenv
import asyncio


load_dotenv()
endpoint = os.getenv("AZURE_ENDPOINT")
Api_key = os.getenv("API_KEY")
apiVersion = os.getenv("OPENAI_API_VERSION")

client = AzureOpenAIChatCompletionClient(
    azure_depoyment_id="gpt-4o",
    model="gpt-4o",
    api_version= apiVersion,
    azure_endpoint=endpoint,
    api_key = Api_key,
    # model_context=BufferedChatCompletionContext(buffer_size=5),
)

assistant = AssistantAgent(
    "assistant",
    model_client= client
)

user = UserProxyAgent(
    "user",
    input_func=input
)


termination = TextMentionTermination("APPROVE")

team = RoundRobinGroupChat([assistant, user], termination_condition= termination)



async def main():
    user_input = input("Agent ask for input: ")
    stream = team.run_stream(task=user_input)
    await Console(stream)
# asyncio.run(await Console(stream))

if __name__ == '__main__':
    asyncio.run(main())