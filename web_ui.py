#!/usr/bin/env python3
import asyncio
import datetime
import threading
import uuid
from collections import defaultdict
from queue import Queue
import json
from flask import Flask, render_template, request, jsonify
import os
from threading import Thread

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv(verbose=True)
    print("Loaded environment from .env file")
except ImportError:
    print("python-dotenv not installed, environment variables must be set manually")

# Check if API key is available
api_key = os.environ.get("ANTHROPIC_API_KEY")
if api_key:
    print("Found ANTHROPIC_API_KEY in environment variables")
else:
    print("="*80)
    print("WARNING: ANTHROPIC_API_KEY environment variable not found.")
    print("To use Claude for agent processing, please set your API key:")
    print("  export ANTHROPIC_API_KEY=your_api_key_here")
    print("="*80)

from nvidia_sales_agent.orchestrator import OrchestratorAgent
from nvidia_sales_agent.product_agent import ProductCatalogAgent
from nvidia_sales_agent.claude_helper import ClaudeClient

app = Flask(__name__)

# In-memory storage for agent sessions
agent_sessions = {}

# Define product domains
product_domains = [
    "GeForce Gaming GPUs",
    "RTX Professional GPUs",
    "NVIDIA Data Center Solutions",
    "CUDA & Developer Tools",
    "AI & Deep Learning Platforms",
    "Networking & DPUs",
    "Automotive & Self-Driving Tech",
    "Cloud Gaming Services"
]

class UINotifier:
    """
    Handles notifying the UI of events via a notification queue.
    """
    def __init__(self, session_id, notification_queue):
        self.session_id = session_id
        self.notification_queue = notification_queue
        
    def notify(self, notification):
        """Add a notification to the queue"""
        notification["session_id"] = self.session_id
        self.notification_queue.put(notification)

class SalesAgentSession:
    """
    Manages a single user session with the sales agent system.
    """
    def __init__(self, session_id, notification_queue):
        self.session_id = session_id
        self.notification_queue = notification_queue
        self.ui_notifier = UINotifier(session_id, notification_queue)
        
        # Log initial session creation
        self.ui_notifier.notify({
            "type": "system",
            "message": "Setting up NVIDIA Sales Agent...",
            "timestamp": datetime.datetime.now().isoformat()
        })
        
    def create_agents(self):
        """
        Create product catalog agents and orchestrator
        """
        # Create Claude client
        try:
            # Try to create a Claude client
            claude_client = ClaudeClient()
            using_claude = True
        except ValueError:
            # Fallback if no API key is available
            claude_client = None
            using_claude = False
            
        # Create product catalog agents for each domain
        agents = {}
        for domain in product_domains:
            agents[domain] = ProductCatalogAgent(domain, claude_client=claude_client)
            
        # Create orchestrator that will coordinate the agents
        orchestrator = OrchestratorAgent(self.ui_notifier, claude_client=claude_client)
        
        # Register all agents with the orchestrator
        for agent_id, agent in agents.items():
            orchestrator.register_agent(agent_id, agent)
            
        self.orchestrator = orchestrator
        
        # Notify that setup is complete
        if using_claude:
            message = "NVIDIA Sales Agent ready with Claude integration"
        else:
            message = "NVIDIA Sales Agent ready (without Claude integration)"
            
        self.ui_notifier.notify({
            "type": "system",
            "message": message,
            "timestamp": datetime.datetime.now().isoformat()
        })
        
    async def process_query(self, query):
        """
        Process a user query through the orchestrator
        """
        return await self.orchestrator.process_query(query)

# Queue to store notifications for each session
notification_queues = defaultdict(Queue)

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/session', methods=['POST'])
def api_create_session():
    """Create a new session"""
    # Generate a session ID
    session_id = str(uuid.uuid4())
    
    # Create notification queue for this session
    notification_queues[session_id] = Queue()
    
    # Define function to initialize session with proper event loop
    def init_session():
        # Set up a new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Create the session with the notification queue
        session = SalesAgentSession(session_id, notification_queues[session_id])
        session.create_agents()
        
        # Store the session
        agent_sessions[session_id] = session
    
    # Run initialization in a separate thread
    init_thread = Thread(target=init_session)
    init_thread.start()
    init_thread.join()  # Wait for initialization to complete
    
    return jsonify({"session_id": session_id})

@app.route('/api/query', methods=['POST'])
def api_query():
    """Process a user query"""
    data = request.json
    session_id = data.get('session_id')
    query = data.get('query')
    
    if not session_id or not query:
        return jsonify({
            "error": "Missing session_id or query"
        }), 400
        
    if session_id not in agent_sessions:
        return jsonify({
            "error": "Invalid session_id"
        }), 404
        
    # Process query asynchronously
    def process():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        session = agent_sessions[session_id]
        response = loop.run_until_complete(session.process_query(query))
        
        # Add final response to notification queue
        notification_queues[session_id].put({
            "type": "response",
            "message": response,
            "session_id": session_id,
            "timestamp": datetime.datetime.now().isoformat()
        })
        
    Thread(target=process).start()
    
    return jsonify({"status": "processing"})

@app.route('/api/notifications', methods=['GET'])
def api_get_notifications():
    """Get notifications for a session"""
    session_id = request.args.get('session_id')
    
    if not session_id:
        return jsonify({
            "error": "Missing session_id"
        }), 400
        
    if session_id not in notification_queues:
        return jsonify({
            "error": "Invalid session_id"
        }), 404
        
    # Get all notifications from the queue
    notifications = []
    queue = notification_queues[session_id]
    
    while not queue.empty():
        notifications.append(queue.get())
        
    return jsonify({"notifications": notifications})

if __name__ == '__main__':
    # Ensure template directory exists
    os.makedirs('templates', exist_ok=True)
    
    # Run the app
    app.run(debug=True, port=8000)
