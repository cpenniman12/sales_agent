import asyncio
import datetime
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
    Simulates UI updates by printing notifications.
    In a real application, this would update the UI components.
    """
    notif_type = notification["type"]
    timestamp = datetime.datetime.fromisoformat(notification["timestamp"]).strftime("%H:%M:%S")
    
    if notif_type == "agent_invocation":
        print(f"[{timestamp}] 🔍 {notification['message']}")
    elif notif_type == "agent_completion":
        print(f"[{timestamp}] ✓ {notification['message']} (Status: {notification['status']})")
    elif notif_type == "follow_up_calls":
        print(f"[{timestamp}] 🔄 {notification['message']}")
    elif notif_type == "orchestrator_thinking":
        print(f"[{timestamp}] 💭 {notification['message']}")

async def main():
    # Initialize the UI notifier
    notifier = UINotifier(ui_callback)
    
    # Initialize the orchestrator
    orchestrator = OrchestratorAgent(notifier)
    
    # Create product agents
    geforce_agent = ProductCatalogAgent("GeForce Gaming GPUs", GEFORCE_KNOWLEDGE)
    rtx_pro_agent = ProductCatalogAgent("RTX Professional GPUs", RTX_PROFESSIONAL_KNOWLEDGE)
    datacenter_agent = ProductCatalogAgent("NVIDIA Data Center Solutions", DATACENTER_KNOWLEDGE)
    cuda_agent = ProductCatalogAgent("CUDA & Developer Tools", CUDA_KNOWLEDGE)
    ai_agent = ProductCatalogAgent("AI & Deep Learning Platforms", AI_KNOWLEDGE)
    networking_agent = ProductCatalogAgent("Networking & DPUs", NETWORKING_KNOWLEDGE)
    automotive_agent = ProductCatalogAgent("Automotive & Self-Driving Tech", AUTOMOTIVE_KNOWLEDGE)
    cloud_gaming_agent = ProductCatalogAgent("Cloud Gaming Services", CLOUD_GAMING_KNOWLEDGE)
    
    # Register agents with the orchestrator
    orchestrator.register_agent("GeForce Gaming GPUs", geforce_agent)
    orchestrator.register_agent("RTX Professional GPUs", rtx_pro_agent)
    orchestrator.register_agent("NVIDIA Data Center Solutions", datacenter_agent)
    orchestrator.register_agent("CUDA & Developer Tools", cuda_agent)
    orchestrator.register_agent("AI & Deep Learning Platforms", ai_agent)
    orchestrator.register_agent("Networking & DPUs", networking_agent)
    orchestrator.register_agent("Automotive & Self-Driving Tech", automotive_agent)
    orchestrator.register_agent("Cloud Gaming Services", cloud_gaming_agent)
    
    # Example queries to test the system
    test_queries = [
        "Tell me about the GeForce RTX 4090",
        "What NVIDIA solutions are available for AI training?",
        "Compare gaming GPUs and professional GPUs",
        "What's the best NVIDIA GPU for machine learning development?",
        "Tell me about NVIDIA's self-driving car technology"
    ]
    
    for query in test_queries:
        print(f"\n[USER] {query}")
        response = await orchestrator.process_query(query)
        print(f"\n[RESPONSE]\n{response}")
        print("\n" + "-"*80)

if __name__ == "__main__":
    asyncio.run(main())
