from dataclasses import dataclass
import asyncio
import os
from dotenv import load_dotenv
# Create the runtime and register the agent.
from autogen_core import AgentId
from autogen_core import MessageContext, RoutedAgent, SingleThreadedAgentRuntime, message_handler
from autogen_core.models import ChatCompletionClient, SystemMessage, UserMessage
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient


load_dotenv()
endpoint = os.getenv("AZURE_ENDPOINT")
Api_key = os.getenv("API_KEY")
apiVersion = os.getenv("OPENAI_API_VERSION")

@dataclass
class Message:
    content: str


class SimpleAgent(RoutedAgent):
    def __init__(self, model_client: ChatCompletionClient) -> None:
        super().__init__("A simple agent")
        self._system_messages = [SystemMessage(content="You are a helpful AI assistant.")]
        self._model_client = model_client

    @message_handler
    async def handle_user_message(self, message: Message, ctx: MessageContext) -> Message:
        # Prepare input to the chat completion model.
        user_message = UserMessage(content=message.content, source="user")
        response = await self._model_client.create(
            self._system_messages + [user_message], cancellation_token=ctx.cancellation_token
        )
        # Return with the model's response.
        assert isinstance(response.content, str)
        return Message(content=response.content)
    


runtime = SingleThreadedAgentRuntime()
async def main():
    await SimpleAgent.register(
        runtime,
        "simple_agent",
        lambda: SimpleAgent(
            AzureOpenAIChatCompletionClient(
                azure_depoyment_id="gpt-4o",
                model="gpt-4o",
                api_version= apiVersion,
                azure_endpoint=endpoint,
                api_key = Api_key,
            )
        ),
    )
    # Start the runtime processing messages.
    runtime.start()
    # Send a message to the agent and get the response.
    message = Message("Hello, what are some fun things to do in Seattle?")
    response = await runtime.send_message(message, AgentId("simple_agent", "default"))
    print(response.content)
    # Stop the runtime processing messages.
    await runtime.stop()


if __name__ == "__main__":
    asyncio.run(main())