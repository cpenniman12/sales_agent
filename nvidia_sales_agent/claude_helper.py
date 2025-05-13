import os
import asyncio
import json
import httpx
import time
from typing import Dict, Any, List, Optional

# Try to import from .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Get API key from environment variable
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

class ClaudeClient:
    """
    Helper class to interact with Claude API for the NVIDIA Sales Agent
    """
    
    def __init__(self, model="claude-3-sonnet-20240229"):
        """
        Initialize the Claude client
        
        Args:
            model: The Claude model to use
        """
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        self.model = model
        self.base_url = "https://api.anthropic.com/v1"
        self.headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
    async def get_completion(self, prompt: str, 
                            system_prompt: Optional[str] = None,
                            temperature: float = 0.7,
                            max_tokens: int = 1000) -> str:
        """
        Get a completion from Claude
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
            
        Returns:
            str: Claude's completion
        """
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
            
        request_body = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        if system_prompt:
            request_body["system"] = system_prompt
            
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/messages",
                    headers=self.headers,
                    json=request_body,
                    timeout=30
                )
                
                response_data = response.json()
                
                if response.status_code != 200:
                    error_message = f"API request failed with status {response.status_code}: {response.text}"
                    print(error_message)
                    raise Exception(error_message)
                    
                return response_data["content"][0]["text"]
                
        except Exception as e:
            print(f"Error calling Claude API: {e}")
            raise 