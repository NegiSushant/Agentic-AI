import pandas as pd
import asyncio
from autogen_core import CancellationToken
from autogen_ext.tools.langchain import LangChainToolAdapter
from langchain_experimental.tools.python.tool import PythonAstREPLTool
from Client_initialization import client
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.ui import Console

df = pd.read_csv("https://raw.githubusercontent.com/pandas-dev/pandas/main/doc/data/titanic.csv")

tool = LangChainToolAdapter(PythonAstREPLTool(locals={"df": df}))
model_clients = client

agent = AssistantAgent(
    "assistant",
    tools=[tool],
    model_client=model_clients,
    system_message="Use the `df` variable to access the dataset.",
)

async def toolsCall():
    response = await agent.on_messages(
        [TextMessage(content="What's the average age of the passengers?", source="user")],
        cancellation_token=CancellationToken(),
    )
    return response.inner_messages, response.chat_message

    # response =   await Console(
    #     agent.on_messages_stream(
    #         [TextMessage(content="What's the average age of the passengers?", source="user")],
    #         CancellationToken(),
    #     )
    # )
    # return response
async def main():
    response_mess,  res_chat_mess = await toolsCall()
    print(response_mess, res_chat_mess)
    # asyncio.run(print(toolsCall()))

if __name__ == "__main__":
    asyncio.run(main())