# Evolve Agents Framework Examples

This directory contains example applications demonstrating how to use the Evolve Agents Framework.

## Chat with Agent Example

The `chat_with_agent.py` script demonstrates how to use the client library to interact with an agent service.

### Prerequisites

1. Make sure you have an agent service running (e.g., evo-concierge)
2. Install the required dependencies:
```bash
pip install aiohttp
```

### Basic Usage

Make the script executable:
```bash
chmod +x chat_with_agent.py
```

Send a simple message to the agent:
```bash
./chat_with_agent.py -m "Hello, how can you help me?"
```

### Command Line Options

- `--url`: Base URL of the agent service (default: http://localhost:8000)
- `--message` or `-m`: Message to send to the agent (required)
- `--context` or `-c`: Optional context information

### Examples

1. Basic message:
```bash
./chat_with_agent.py -m "What services do you provide?"
```

2. Message with context:
```bash
./chat_with_agent.py -m "What can you tell me about this?" -c "This is a document about machine learning algorithms"
```

3. Using a different agent service URL:
```bash
./chat_with_agent.py --url http://other-agent:8000 -m "Hello"
```

4. Combining options:
```bash
./chat_with_agent.py \
    --url http://agent-service:8000 \
    -m "Analyze this content" \
    -c "Important context information"
```

### Example Output

```
Agent status: idle

Agent response:
----------------------------------------
I am an AI assistant that can help you with various tasks. I can answer questions,
provide information, and help you navigate through the Evolve system. How may I
assist you today?
----------------------------------------
```

### Error Handling

The script handles various error cases:

1. Agent service not available:
```
Error communicating with agent: Cannot connect to host localhost:8000
```

2. Invalid response:
```
Error: Agent returned error status
```

### Tips

1. Use quotes around messages or context that contain spaces:
```bash
./chat_with_agent.py -m "This is a multi-word message"
```

2. For complex context, you can read from a file:
```bash
./chat_with_agent.py -m "Analyze this" -c "$(cat context.txt)"
```

3. For Windows users, use python directly:
```bash
python chat_with_agent.py -m "Hello"
```

## Coming Soon

More examples will be added to demonstrate:
- Interactive chat sessions
- Work request processing
- Custom agent implementations
- Integration patterns 