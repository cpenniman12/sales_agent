# NVIDIA Sales Agent

An intelligent sales agent powered by an agentic architecture that provides information about NVIDIA products.

## Project Overview

This project implements a conversational agent that uses multiple specialized Product Catalog Agents coordinated by an Orchestrator Agent to answer queries about NVIDIA products. The system provides real-time UI feedback on agent invocations and processes unstructured product knowledge to generate comprehensive responses.

## Architecture

### Core Components

1. **Orchestrator Agent**
   - Central coordinator that analyzes queries, selects appropriate agents, and combines responses
   - Makes decisions about which Product Catalog Agents to consult
   - Dispatches requests to multiple agents in parallel
   - Provides real-time UI notifications of agent activities
   - Determines when follow-up agent calls are needed
   - Synthesizes comprehensive responses from agent inputs

2. **Product Catalog Agents**
   - Specialized agents for 8 different NVIDIA product domains:
     * GeForce Gaming GPUs
     * RTX Professional GPUs
     * NVIDIA Data Center Solutions
     * CUDA & Developer Tools
     * AI & Deep Learning Platforms
     * Networking & DPUs
     * Automotive & Self-Driving Tech
     * Cloud Gaming Services
   - Process queries against unstructured product knowledge
   - Generate domain-specific responses
   - Provide confidence scores for responses

3. **UI Notification System**
   - Provides real-time feedback on agent activities
   - Notifies users when agents are invoked
   - Shows completion status for agent operations
   - Indicates when follow-up agent calls are needed

## Installation

```bash
# Clone the repository
git clone https://github.com/cpenniman12/sales_agent.git
cd sales_agent

# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package and dependencies
pip install -e .
```

## Usage

### Web User Interface

Run the web-based UI to interact with the NVIDIA Sales Agent through your browser:

```bash
python web_ui.py
```

Then open your browser and navigate to `http://127.0.0.1:5000/` to access the interface.

The web UI features:
- Chat interface for asking questions about NVIDIA products
- Real-time notifications showing which agents are being consulted
- Agent activity log that displays the behind-the-scenes processing

### Interactive Command Line Mode

Run the agent in interactive mode to ask questions about NVIDIA products:

```bash
python main.py
```

This starts an interactive session where you can type queries and receive responses with real-time UI notifications of agent activities.

### Demo Mode

Run the agent with predefined demo queries:

```bash
python main.py --demo
```

This processes a series of predefined queries that demonstrate the capabilities of the system.

### Example Code

You can also use the example script to see how multiple queries are processed:

```bash
python example.py
```

This script runs through a series of test queries and shows how the architecture works.

## Extending the System

### Adding New Product Knowledge

To update or expand the product knowledge:

1. Edit the files in `nvidia_sales_agent/knowledge/` or add new ones
2. Update the knowledge variables like `GEFORCE_KNOWLEDGE` with new information

### Enhancing Agent Selection Logic

To improve how the Orchestrator selects agents:

1. Modify the `_select_agents` method in the `OrchestratorAgent` class
2. Update the keyword-based selection rules in the agent initialization

### Improving Response Generation

To enhance the quality of responses:

1. Modify the `_generate_response` method in the `ProductCatalogAgent` class
2. Enhance the information retrieval logic in `_retrieve_information`
3. Update the confidence scoring algorithm in `_calculate_confidence`

## Example Queries

Try these example queries to test the system:

- "What's the best NVIDIA GPU for gaming?"
- "Tell me about the GeForce RTX 4090"
- "Compare RTX professional GPUs with gaming GPUs"
- "What NVIDIA solutions are available for AI training?"
- "How does NVIDIA support self-driving cars?"
- "Tell me about NVIDIA's cloud gaming service"
- "What are the features of CUDA?"
- "What networking solutions does NVIDIA offer?"

## Future Enhancements

- Integration with a Large Language Model for more sophisticated responses
- Persistent conversation history and context tracking
- Multi-modal interactions with product images and diagrams
- Enhanced analytics on agent performance and utilization
- Support for personalized product recommendations

## License

This project is for demonstration purposes only.

## Credits

This project was created as a proof of concept for an agentic architecture in customer-facing applications. It demonstrates how specialized agents can collaborate to provide comprehensive responses to user queries.
