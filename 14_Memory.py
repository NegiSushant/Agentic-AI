# add: add new entries to the memory store
# query: retrieve relevant information from the memory store
# update_context: mutate an agent’s internal model_context by adding the retrieved information (used in the AssistantAgent class)
# clear: clear all entries from the memory store
# close: clean up any resources used by the memory store

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_core.memory import ListMemory, MemoryContent, MemoryMimeType
from Client_initialization import client


user_memory = ListMemory()
# Initialize user memory
def initMemo():
    
    user_memory.add(MemoryContent(content="The weather should be in metric units", mime_type=MemoryMimeType.TEXT))

    user_memory.add(MemoryContent(content="Meal recipe must be vegan", mime_type=MemoryMimeType.TEXT))
    return user_memory



async def get_weather(city: str, units: str = "imperial") -> str:
    if units == "imperial":
        return f"The weather in {city} is 73 °F and Sunny."
    elif units == "metric":
        return f"The weather in {city} is 23 °C and Sunny."
    else:
        return f"Sorry, I don't know the weather in {city}."


assistant_agent = AssistantAgent(
    name="assistant_agent",
    model_client=client,
    tools=[get_weather],
    memory=[user_memory],
)


async def main():
    # Add user preferences to memory

    stream = assistant_agent.run_stream(task="What is the weather in New York?")
    await Console(stream)