#!/usr/bin/env python3
import asyncio
import argparse
from pathlib import Path
from typing import List, Optional
from core.client import HttpAgentClient
from core.schemas import WorkRequest, MessageHistory
import aiohttp
import json


async def upload_file_to_agent(
    base_url: str,
    file_path: str,
    task: str,
    context: str = "",
    history: Optional[List[MessageHistory]] = None
):
    """Upload a file to an agent and process it"""
    
    if history is None:
        history = []
    
    # Create work request object
    work_request = WorkRequest(
        task=task,
        context=context,
        history=history
    )
    
    file_path = Path(file_path)
    if not file_path.exists():
        print(f"Error: File {file_path} does not exist")
        return

    # Determine content type based on file extension
    content_type_map = {
        '.txt': 'text/plain',
        '.pdf': 'application/pdf',
        '.doc': 'application/msword',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.csv': 'text/csv',
        '.json': 'application/json'
    }

    extension = file_path.suffix.lower()
    content_type = content_type_map.get(extension, 'application/octet-stream')
    
    # Use context manager to handle session lifecycle
    async with HttpAgentClient(base_url) as client:
        try:
            # Check agent status
            status = await client.get_status()
            print(f"Agent status: {status['status']}")
            
            # Upload file and get initial response
            with open(file_path, 'rb') as file:
                response = await client.process_work_request_with_file(
                    work_request=work_request,
                    file=file,
                    filename=file_path.name,
                    content_type=content_type
                )
            
            print(f"\nWork request started with ID: {response.work_id}")
            print(f"Initial status: {response.status}")
            
            # Poll for completion if the work is async
            while response.status in ['pending', 'in_progress']:
                print(f"Status: {response.status}... waiting")
                await asyncio.sleep(2)  # Wait 2 seconds between checks
                
                response = await client.get_work_result(response.work_id)
                if not response:
                    print("Error: Work request not found")
                    return
            
            # Print final result
            print("\nFinal result:")
            print("-" * 40)
            if response.status == "completed":
                print(response.result)
            else:
                print(f"Error: {response.error}")
            print("-" * 40)
                
        except Exception as e:
            print(f"Error communicating with agent: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Upload a file to an Evolve agent")
    parser.add_argument(
        "--url", 
        default="http://localhost:8000",
        help="Base URL of the agent service (default: http://localhost:8000)"
    )
    parser.add_argument(
        "--file", "-f",
        required=True,
        help="Path to the file to upload"
    )
    parser.add_argument(
        "--task", "-t",
        required=True,
        help="Task description for processing the file"
    )
    parser.add_argument(
        "--context", "-c",
        default="",
        help="Optional context information"
    )
    
    args = parser.parse_args()
    
    # Run the async function
    asyncio.run(upload_file_to_agent(
        base_url=args.url,
        file_path=args.file,
        task=args.task,
        context=args.context
    ))

if __name__ == "__main__":
    main() 