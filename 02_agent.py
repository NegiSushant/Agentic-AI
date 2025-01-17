#Agents attributes and Method
# name:  The unique name of the agent in text
# description: description of the agent in text
# on_messages(): Send the agent a sequence of ChatMessage get a Response. It is important to note that agents are expected to be stateful and this method is expected to be called with new messages, not the complete history
#on_message_stream(): Same as on_messages() but returns an iterator of AgentEvent or ChatMessage followed by a Response as the last item.
# on_reset(): Reset the agent to its initial state
# run() and run_stream(): convience methods that on_messages() and on_messages_stream() respectively but offer the same interface as Teams

# Assistant agent 
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from dotenv import load_dotenv
import asyncio
import os


load_dotenv()
endpoint = os.getenv("AZURE_ENDPOINT")
Api_key = os.getenv("API_KEY")
apiVersion = os.getenv("OPENAI_API_VERSION")


async def web_serch(query: str) -> str:
    """Find information on the web"""
    return "Autogen is a Programing framework for building multi-agent applications."

client = AzureOpenAIChatCompletionClient(
    azure_depoyment_id="gpt-4o",
    model="gpt-4o",
    api_version= apiVersion,
    azure_endpoint=endpoint,
    # AZURE_OPENAI_API_KEY = Api_key
    api_key = Api_key
)

agent = AssistantAgent(
    name="assistent",
    model_client = client,
    tools=[web_serch],
    system_message = "Use tools to solve tasks."
)

# getting the responses
async def assistant_run():
    response = await agent.on_messages(
        [TextMessage(content="Find information on AutoGen", source="user")],
        cancellation_token=CancellationToken(),
    )
    return response.inner_messages, response.chat_message
async def assistant_run2():
    # Option 2: use Console to print all messages as they appear.
    await Console(
        agent.on_messages_stream(
            [TextMessage(content="Find information on AutoGen", source="user")],
            cancellation_token=CancellationToken(),
        )
    )

# asyncio.run(assistant_run2())
async def main():
    response_mess,  res_chat_mess = await assistant_run()
    print(response_mess, res_chat_mess)

if __name__ == "__main__":
    asyncio.run(main())