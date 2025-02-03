from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from Client_initialization import client


agent = AssistantAgent(
    name="assistant",
    model_client=client,
    handoffs=["flights_refunder", "user"],
    # tools=[], # serializing tools is not yet supported
    system_message="Use tools to solve tasks.",
)
user_proxy = UserProxyAgent(name="user")

user_proxy_config = user_proxy.dump_component()  # dump component
print(user_proxy_config.model_dump_json())
up_new = user_proxy.load_component(user_proxy_config)  # load component


agent_config = agent.dump_component()  # dump component
print(agent_config.model_dump_json())
agent_new = agent.load_component(agent_config)  # load component