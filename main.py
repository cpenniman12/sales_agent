import asyncio
import sys
from nvidia_sales_agent.orchestrator import OrchestratorAgent
from nvidia_sales_agent.product_agent import ProductCatalogAgent
from nvidia_sales_agent.ui_notifier import UINotifier

# Import knowledge bases
from nvidia_sales_agent.knowledge.geforce import GEFORCE_KNOWLEDGE
from nvidia_sales_agent.knowledge.rtx_professional import RTX_PROFESSIONAL_KNOWLEDGE
from nvidia_sales_agent.knowledge.datacenter import DATACENTER_KNOWLEDGE
from nvidia_sales_agent.knowledge.cuda import CUDA_KNOWLEDGE
from nvidia_sales_agent.knowledge.ai_platforms import AI_KNOWLEDGE
from nvidia_sales_agent.knowledge.networking import NETWORKING_KNOWLEDGE
from nvidia_sales_agent.knowledge.automotive import AUTOMOTIVE_KNOWLEDGE
from nvidia_sales_agent.knowledge.cloud_gaming import CLOUD_GAMING_KNOWLEDGE

def ui_callback(notification):
    """
    Handle UI notifications by printing them with appropriate formatting.
    In a real application, this would update UI components.
    """
    notif_type = notification["type"]
    
    if notif_type == "agent_invocation":
        print(f"🔍 {notification['message']}")
    elif notif_type == "agent_completion":
        print(f"✓ {notification['message']} (Status: {notification['status']})")
    elif notif_type == "follow_up_calls":
        print(f"🔄 {notification['message']}")
    elif notif_type == "orchestrator_thinking":
        print(f"💭 {notification['message']}")
    
    # Ensure the notification is immediately visible
    sys.stdout.flush()

class NVIDIASalesAgent:
    """
    Main class for the NVIDIA Sales Agent that coordinates all components.
    """
    def __init__(self):
        # Initialize the UI notifier
        self.notifier = UINotifier(ui_callback)
        
        # Initialize the orchestrator
        self.orchestrator = OrchestratorAgent(self.notifier)
        
        # Initialize and register all product agents
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize all product catalog agents and register them with the orchestrator."""
        # Create product agents
        agents = [
            ("GeForce Gaming GPUs", GEFORCE_KNOWLEDGE),
            ("RTX Professional GPUs", RTX_PROFESSIONAL_KNOWLEDGE),
            ("NVIDIA Data Center Solutions", DATACENTER_KNOWLEDGE),
            ("CUDA & Developer Tools", CUDA_KNOWLEDGE),
            ("AI & Deep Learning Platforms", AI_KNOWLEDGE),
            ("Networking & DPUs", NETWORKING_KNOWLEDGE),
            ("Automotive & Self-Driving Tech", AUTOMOTIVE_KNOWLEDGE),
            ("Cloud Gaming Services", CLOUD_GAMING_KNOWLEDGE)
        ]
        
        # Create and register each agent
        for agent_id, knowledge_base in agents:
            agent = ProductCatalogAgent(agent_id, knowledge_base)
            self.orchestrator.register_agent(agent_id, agent)
    
    async def process_query(self, query):
        """Process a user query and return the response."""
        return await self.orchestrator.process_query(query)

async def interactive_mode():
    """Run the sales agent in interactive mode where users can type queries."""
    print("NVIDIA Sales Agent - Interactive Mode")
    print("Type 'exit' or 'quit' to end the session.")
    print("-" * 50)
    
    # Initialize the sales agent
    agent = NVIDIASalesAgent()
    
    while True:
        # Get user input
        user_input = input("\nYou: ")
        
        # Check for exit command
        if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
            print("Thank you for using the NVIDIA Sales Agent. Goodbye!")
            break
        
        # Process the query
        print("\nNVIDIA Sales Agent:")
        response = await agent.process_query(user_input)
        print(f"\n{response}")

async def demo_mode():
    """Run the sales agent in demo mode with predefined queries."""
    print("NVIDIA Sales Agent - Demo Mode")
    print("-" * 50)
    
    # Initialize the sales agent
    agent = NVIDIASalesAgent()
    
    # Predefined demo queries
    demo_queries = [
        "What's the best NVIDIA GPU for gaming?",
        "Tell me about NVIDIA's AI solutions",
        "How does NVIDIA support self-driving cars?",
        "What are the benefits of RTX technology?",
        "Tell me about NVIDIA's cloud gaming service"
    ]
    
    # Process each query
    for i, query in enumerate(demo_queries, 1):
        print(f"\nDemo Query {i}: {query}")
        print("\nNVIDIA Sales Agent:")
        response = await agent.process_query(query)
        print(f"\n{response}")
        
        # Add a pause between queries for demo purposes
        if i < len(demo_queries):
            print("\n" + "-" * 50)
            input("Press Enter for next demo query...")
    
    print("\nDemo completed! Thank you for using the NVIDIA Sales Agent.")

if __name__ == "__main__":
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="NVIDIA Sales Agent")
    parser.add_argument("--demo", action="store_true", help="Run in demo mode with predefined queries")
    args = parser.parse_args()
    
    # Run in the appropriate mode
    if args.demo:
        asyncio.run(demo_mode())
    else:
        asyncio.run(interactive_mode())
