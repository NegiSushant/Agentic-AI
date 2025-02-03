from autogen_agentchat.conditions import MaxMessageTermination, StopMessageTermination

max_termination = MaxMessageTermination(5)
stop_termination = StopMessageTermination()

or_termination = max_termination | stop_termination

or_term_config = or_termination.dump_component()
print("Config: ", or_term_config.model_dump_json())

new_or_termination = or_termination.load_component(or_term_config)