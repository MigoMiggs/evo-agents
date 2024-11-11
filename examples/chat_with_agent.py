#!/usr/bin/env python3
import asyncio
import argparse
from typing import List, Optional
from core.client import HttpAgentClient
from core.schemas import Message, MessageHistory

async def chat_with_agent(
    base_url: str,
    message: str,
    context: str = "",
    history: Optional[List[MessageHistory]] = None
):
    """Send a message to an agent and print the response"""
    
    if history is None:
        history = []
    
    # Create message object
    msg = Message(
        message=message,
        role="user",
        context=context,
        history=history
    )
    
    # Use context manager to handle session lifecycle
    async with HttpAgentClient(base_url) as client:
        try:
            # Check agent status
            status = await client.get_status()
            print(f"Agent status: {status['status']}")
            
            # Send message and get response
            response = await client.process_message(msg)
            
            if response.status == "completed":
                print("\nAgent response:")
                print("-" * 40)
                print(response.result)
                print("-" * 40)
            else:
                print(f"\nError: {response.error}")
                
        except Exception as e:
            print(f"Error communicating with agent: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Chat with an Evolve agent")
    parser.add_argument(
        "--url", 
        default="http://localhost:8000",
        help="Base URL of the agent service (default: http://localhost:8000)"
    )
    parser.add_argument(
        "--message", "-m",
        required=True,
        help="Message to send to the agent"
    )
    parser.add_argument(
        "--context", "-c",
        default="",
        help="Optional context information"
    )
    
    args = parser.parse_args()
    
    # Run the async function
    asyncio.run(chat_with_agent(
        base_url=args.url,
        message=args.message,
        context=args.context
    ))

if __name__ == "__main__":
    main() 