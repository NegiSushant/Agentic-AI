# when user or application intracts with the team of agents in an interactive loop like:
* the team runs until termination
* the application and user provides feedback
* team run again with the feedback

This approach is useful in a persisted session with asynchronous communication between the team and the application/user: Once a team finishes a run, the application saves the state of the team, puts it in a persistent storage, and resumes the team when the feedback arrives.


# There are two way to implement this approach:
* Set the maximum number of turns so that the team always stops after the specific number of turns.
* User termination conditions such as TextMentionTermination and HandoffTermination to allow the team to decide when to stop and give control back, given the team's internal state

