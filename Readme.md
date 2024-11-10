# Evolve Agents Framework

This is the agents framework repo. This repo shows how to implement an evo system agent. Each agent is composed as separate FastAPI app. 

Every agent has the same structure. Every agent is a fast api service that exposes the following endpoints:

- 'POST /agent/restart' - starts the agent
- 'POST /agent/message' - send a message to the agent, it expects a json with the following fields:
    - 'message' - the message to send to the agent
    - 'role' - the role of the message sender
    - 'context' - the context of the message sender
    - 'history' - the history of the message sender, this is a list of messages in the following format: [{'role': 'user', 'content': 'Hello, how are you?'}, {'role': 'assistant', 'content': 'I am fine, thank you!'}]
    - this endpoint returns a json with the following fields:
        - 'status' - the status of the message, this can be 'pending', 'in_progress', 'completed', 'failed'
        - 'result' - the result of the message, which is expressed in english
        - 'error' - the error of the message
- 'GET /agent/status' - get the agent status
- 'POST /agent/work-request' - send a work request to the agent, it expects a json with the following fields:
    - 'task' - the task to send to the agent
    - 'context' - the context of the task
    - 'history' - the history relevant to the task, this is a list of messages in the following format: [{'role': 'user', 'content': 'Hello, how are you?'}, {'role': 'assistant', 'content': 'I am fine, thank you!'}]
    - this endpoint returns a json with the following fields:
        - 'status' - the status of the work request, this can be 'pending', 'in_progress', 'completed', 'failed'
        - 'result' - the result of the work request, which is expressed in english
        - 'error' - the error of the work request


