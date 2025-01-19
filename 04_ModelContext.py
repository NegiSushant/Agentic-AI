# AssistantAgent has a model_context parameter that can be used to pass in a ChatCompletionContext object. This allows the agent to use different model contexts, such as BufferedChatCompletionContext to limit the context sent to the model.

# By default, AssistantAgent uses the UnboundedChatCompletionContext which sends the full conversation history to the model. To limit the context to the last n messages, you can use the BufferedChatCompletionContext.

# The following example demonstrates how to use the BufferedChatCompletionContext with AssistantAgent:
from autogen_core.model_context import BufferedChatCompletionContext

# Create an agent that uses only the last 5 messages in the context to generate responses.
agent = AssistantAgent(
    name="assistant",
    model_client=model_client,
    tools=[web_search],
    system_message="Use tools to solve tasks.",
    model_context=BufferedChatCompletionContext(buffer_size=5),  # Only use the last 5 messages in the context.
)