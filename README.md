# NVIDIA Sales Agent

An intelligent sales agent powered by an agentic architecture that provides information about NVIDIA products.

## Project Overview

This project implements a conversational agent that uses multiple specialized Product Catalog Agents coordinated by an Orchestrator Agent to answer queries about NVIDIA products. The system provides real-time UI feedback on agent invocations and processes unstructured product knowledge to generate comprehensive responses.

## Architecture

- **Orchestrator Agent**: Central coordinator that analyzes queries, selects appropriate agents, and combines responses
- **Product Catalog Agents**: Specialized agents for different NVIDIA product lines
- **UI Notification System**: Provides real-time feedback on agent activities

## Installation

```bash
git clone https://github.com/cpenniman12/sales_agent.git
cd sales_agent
pip install -r requirements.txt
```

## Usage

```python
from nvidia_sales_agent.orchestrator import OrchestratorAgent
from nvidia_sales_agent.ui_notifier import UINotifier

# Setup UI notifier
notifier = UINotifier(ui_callback_function)

# Create orchestrator
orchestrator = OrchestratorAgent(notifier)

# Process a query
response = orchestrator.process_query("Tell me about the GeForce RTX 4090")
```

## Product Domains

1. GeForce Gaming GPUs
2. RTX Professional GPUs
3. NVIDIA Data Center Solutions
4. CUDA & Developer Tools
5. AI & Deep Learning Platforms
6. Networking & DPUs
7. Automotive & Self-Driving Tech
8. Cloud Gaming Services
