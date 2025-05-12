#!/usr/bin/env python
"""
NVIDIA Sales Agent Demo

This script demonstrates the NVIDIA Sales Agent by processing a specific query
and showing real-time UI notifications as different agents are invoked.
"""

import asyncio
import time
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

def fancy_print(message, style=None):
    """Print a message with fancy formatting"""
    if style == "header":
        print("\n" + "=" * 80)
        print(f"{message:^80}")
        print("=" * 80 + "\n")
    elif style == "subheader":
        print("\n" + "-" * 60)
        print(f"{message:^60}")
        print("-" * 60)
    elif style == "user":
        print(f"\n💬 USER: {message}\n")
    elif style == "agent":
        print(f"\n🤖 NVIDIA AGENT: {message}")
    elif style == "info":
        print(f"\n📌 {message}")
    else:
        print(message)

def ui_callback(notification):
    """
    Handle UI notifications with pretty formatting.
    In a real application, these would update UI components.
    """
    notif_type = notification["type"]
    
    if notif_type == "agent_invocation":
        agent = notification["agent_id"]
        print(f"🔍 Consulting {agent} Agent...")
        # Simulate a slight delay to make the UI notifications more visible
        time.sleep(0.2)
    elif notif_type == "agent_completion":
        agent = notification["agent_id"]
        status = notification["status"]
        print(f"✓ {agent} Agent has responded. (Status: {status})")
        time.sleep(0.2)
    elif notif_type == "follow_up_calls":
        print(f"🔄 {notification['message']}")
        time.sleep(0.2)
    elif notif_type == "orchestrator_thinking":
        print(f"💭 {notification['message']}")
        time.sleep(0.2)

async def run_demo():
    """Run the NVIDIA Sales Agent demo with a specific query"""
    fancy_print("NVIDIA SALES AGENT DEMO", "header")
    fancy_print("This demonstration shows how the NVIDIA Sales Agent uses multiple specialized agents to answer complex queries", "info")
    
    # Initialize the UI notifier
    notifier = UINotifier(ui_callback)
    
    # Initialize the orchestrator
    orchestrator = OrchestratorAgent(notifier)
    
    # Initialize and register product agents
    fancy_print("Initializing Product Catalog Agents...", "subheader")
    
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
    
    for agent_id, knowledge_base in agents:
        print(f"📋 Registering {agent_id} Agent")
        agent = ProductCatalogAgent(agent_id, knowledge_base)
        orchestrator.register_agent(agent_id, agent)
        time.sleep(0.2)  # Slight delay for visual effect
    
    # Define a complex query that will trigger multiple agents
    query = "I'm a data scientist looking for the best NVIDIA solutions for training large language models and deploying them efficiently. What would you recommend?"
    
    fancy_print("Starting the Agent Interaction", "subheader")
    
    # Display the user query
    fancy_print(query, "user")
    
    # Process the query
    print("🔄 Processing query... Watch in real-time as different agents are consulted:")
    print("\n" + "-" * 60)
    
    # Call the orchestrator to process the query
    response = await orchestrator.process_query(query)
    
    print("-" * 60 + "\n")
    
    # Display the final response
    fancy_print("Final Response", "subheader")
    print(response)
    
    # Closing message
    fancy_print("\nDemo completed! This demonstration showed how the orchestrator consulted multiple specialized agents to provide a comprehensive response.", "info")
    fancy_print("The real-time notifications showed which agents were being invoked, making the internal processing visible to the user.", "info")

if __name__ == "__main__":
    asyncio.run(run_demo())
