# Evolve Agents Framework Core

This is the core framework that provides base classes and shared functionality for all Evolve agents. The core framework ensures consistency across different agent implementations while allowing for specialized behavior.

## Structure

```
core/
├── README.md
├── agent_base.py     # Base agent class definition
├── service_base.py   # Base service class for agent operations
└── schemas.py        # Shared data models and schemas
```

## Components

### BaseAgent (agent_base.py)
The abstract base class that all agents must inherit from. It defines the standard interface for agent behavior:

- `process_message()` - Handles incoming messages
- `process_work_request()` - Processes work requests
- `get_state()` - Returns the agent's current state

### BaseAgentService (service_base.py)
Provides common service-level functionality for managing agents:

- `restart()` - Restarts the agent
- `process_message()` - Handles message processing with error handling
- `get_status()` - Returns service status
- `process_work_request()` - Handles work requests with error handling

### Schemas (schemas.py)
Defines the standard data models used across all agents:

- `MessageHistory` - Structure for message history entries
- `Message` - Format for incoming messages
- `WorkRequest` - Format for work requests
- `AgentResponse` - Standard response format

## Usage

1. Create a new agent by inheriting from BaseAgent:

```python
from core.agent_base import BaseAgent

class MyCustomAgent(BaseAgent):
    def process_message(self, message, role, context, history):
        # Implement message processing
        pass

    def process_work_request(self, task, context, history):
        # Implement work request processing
        pass
```

2. Create a service for your agent by inheriting from BaseAgentService:

```python
from core.service_base import BaseAgentService
from .agent import MyCustomAgent

class MyCustomAgentService(BaseAgentService):
    def __init__(self):
        super().__init__(MyCustomAgent())
```

3. Use the standard schemas for data handling:

```python
from core.schemas import Message, WorkRequest, AgentResponse

# Example message handling
message = Message(
    message="Hello",
    role="user",
    context={},
    history=[]
)
```

## Benefits

- **Standardization**: Ensures all agents follow the same interface
- **Code Reuse**: Common functionality is implemented once in the core
- **Error Handling**: Consistent error handling across all agents
- **Type Safety**: Standard schemas ensure data consistency
- **Extensibility**: Easy to add new agent types while maintaining compatibility

## Best Practices

1. Always inherit from BaseAgent when creating new agents
2. Use the provided schemas for data structures
3. Implement error handling in agent-specific code
4. Keep agent-specific logic in the agent class
5. Use the service class for operation management

## Example Implementation

See the `agent-rag-resumes` and `agent-evo-concierge` directories for example implementations using this core framework. 