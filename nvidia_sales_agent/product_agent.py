import os
from .claude_helper import ClaudeClient
from typing import Dict, Any

class ProductCatalogAgent:
    """
    Agent specialized in a specific NVIDIA product domain that answers queries
    with just a brief description of the product line.
    """
    
    def __init__(self, agent_id: str, claude_client=None):
        """
        Initialize a ProductCatalogAgent for a specific product domain.
        
        Args:
            agent_id: Unique identifier representing the product domain
            claude_client: Optional Claude client for API calls
        """
        self.agent_id = agent_id
        self.claude_client = claude_client or ClaudeClient()
        
    async def process_query(self, query: str) -> Dict[str, Any]:
        """
        Process a user query about NVIDIA products in this agent's domain.
        
        Args:
            query: The user's query string
            
        Returns:
            dict: A dictionary containing the response
        """
        # Generate response with Claude using simple product knowledge
        response = await self._generate_response_with_claude(query)
        
        # All agents have equal confidence
        confidence = 0.5
        
        return {
            "agent_id": self.agent_id,
            "response": response,
            "confidence": confidence
        }
    
    async def _generate_response_with_claude(self, query: str) -> str:
        """
        Generate a response to the query using Claude with minimal product information.
        
        Args:
            query: The user's query
            
        Returns:
            str: The generated response
        """
        try:
            # Create simple domain-specific system prompt
            system_prompt = self._get_domain_system_prompt()
            
            # Build the user prompt
            prompt = f"""User query: "{query}"

Please use ONLY the information in your system prompt about NVIDIA {self.agent_id} to answer this query.
Do not make up any specifications or details that weren't provided to you. 
If you don't have enough information to answer fully, be honest about your limitations."""

            # Get Claude's response
            response = await self.claude_client.get_completion(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.3,
                max_tokens=600
            )
            
            return response
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return f"I apologize, I encountered an error while trying to provide information about {self.agent_id}."
    
    def _get_domain_system_prompt(self) -> str:
        """
        Return a simple domain-specific system prompt with just a few sentences.
        
        Returns:
            str: The domain-specific system prompt
        """
        # Base system prompt template with minimal instruction
        system_prompt = f"""You are answering questions about NVIDIA {self.agent_id}. You only know the following few sentences about this product domain:

"""

        # Domain-specific information - just a few sentences for each
        if "GeForce Gaming GPUs" in self.agent_id:
            system_prompt += """
NVIDIA GeForce GPUs are dedicated graphics cards for gaming. The current RTX 40-series includes models like the 4090, 4080, 4070, and 4060, offering features like ray tracing and DLSS. They are designed for gaming performance across different price points."""

        elif "RTX Professional GPUs" in self.agent_id:
            system_prompt += """
NVIDIA RTX Professional GPUs (formerly Quadro) are designed for professional workloads. They include the RTX A-series cards with certified drivers for CAD, 3D modeling, and visualization software. They prioritize accuracy and reliability over gaming performance."""

        elif "Data Center" in self.agent_id:
            system_prompt += """
NVIDIA Data Center solutions include H100, A100, and L40S GPUs for enterprise applications. These power AI, HPC, and data analytics in server environments. NVIDIA DGX systems combine multiple GPUs for advanced AI training and inference."""

        elif "CUDA & Developer" in self.agent_id:
            system_prompt += """
NVIDIA CUDA is a parallel computing platform for developers. It includes the CUDA Toolkit, libraries like cuDNN and TensorRT, and programming APIs. CUDA allows developers to use NVIDIA GPUs for general purpose computing beyond graphics."""

        elif "AI & Deep Learning" in self.agent_id:
            system_prompt += """
NVIDIA's AI platforms support machine learning and deep learning workflows. They include hardware optimized for AI, frameworks like NeMo and Omniverse, and enterprise software solutions. NVIDIA GPUs have tensor cores specifically designed to accelerate AI computations."""

        elif "Networking & DPUs" in self.agent_id:
            system_prompt += """
NVIDIA networking products include ConnectX adapters, BlueField DPUs, and Spectrum switches. They provide high-bandwidth, low-latency networking for data centers. The BlueField DPUs offload networking, security, and storage tasks from CPUs."""

        elif "Automotive" in self.agent_id:
            system_prompt += """
NVIDIA automotive solutions power self-driving vehicles and in-car AI. The DRIVE platform includes Orin processors and software for autonomous driving. These systems handle sensor fusion, path planning, and driver monitoring for vehicle autonomy."""

        elif "Cloud Gaming" in self.agent_id:
            system_prompt += """
NVIDIA GeForce NOW is a cloud gaming service that streams games from NVIDIA servers. It supports various devices including PCs, Macs, mobile, and TVs. Different subscription tiers offer varying levels of performance and features like RTX."""
            
        return system_prompt 