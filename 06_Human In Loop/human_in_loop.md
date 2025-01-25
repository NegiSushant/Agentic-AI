##  this feature used on how to interact with the team from your application and provide human feedback to the team
### There are following two main ways to intract with the team from your application:

- During a team's run - excution of `run()` or `run_stream()` provide feedback through a UserProxyAgent
- Once the run terminates, provide feedback through to the input to the next call to `run()` or `run_stream()`
- # UserProxyAgent is special built in agent that acts as a proxy for a user to provide feedback to the team

* to use the UserProxyAgent, you can create an instance of it and include it in the team before running the team, and the team will decide when to call the UserProxyAgent to ask for the feedback from the user
* When UserProxyAgent is called during a run, it blocks the execution of the team until the user provides feedback or error out. This will hold up the team's progress and put the team in an unstable state that cannot be saved or resumed
* Due to blocking nature of this approach, only used it for short interactions that require immediate feedback from the user such as asking for approval or disapproval with a button click, or an alert requiring immediate atttention otherwise failing the task
