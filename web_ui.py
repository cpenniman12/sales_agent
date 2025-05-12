import asyncio
import json
from flask import Flask, render_template, request, jsonify
from threading import Thread
from queue import Queue

# Import our NVIDIA Sales Agent components
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

app = Flask(__name__)

# Queue to store notifications for each session
notification_queues = {}

# Store the event loop for each session
event_loops = {}

# Custom UI notifier that adds notifications to a queue
class WebUINotifier(UINotifier):
    def __init__(self, session_id):
        self.session_id = session_id
        super().__init__(self._notification_callback)
    
    def _notification_callback(self, notification):
        # Ensure session queue exists
        if self.session_id not in notification_queues:
            notification_queues[self.session_id] = Queue()
        
        # Add notification to the queue
        notification_queues[self.session_id].put(notification)

class SalesAgentSession:
    def __init__(self, session_id):
        self.session_id = session_id
        self.ui_notifier = WebUINotifier(session_id)
        self.orchestrator = OrchestratorAgent(self.ui_notifier)
        self._initialize_agents()
        
    def _initialize_agents(self):
        # Create and register each product agent
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
            agent = ProductCatalogAgent(agent_id, knowledge_base)
            self.orchestrator.register_agent(agent_id, agent)

# Store active agent sessions
agent_sessions = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/session', methods=['POST'])
def create_session():
    # Generate session ID
    import uuid
    session_id = str(uuid.uuid4())
    
    # Create agent session
    agent_sessions[session_id] = SalesAgentSession(session_id)
    
    # Create notification queue
    notification_queues[session_id] = Queue()
    
    return jsonify({'session_id': session_id})

@app.route('/api/query', methods=['POST'])
def process_query():
    data = request.json
    session_id = data.get('session_id')
    query = data.get('query')
    
    if not session_id or session_id not in agent_sessions:
        return jsonify({'error': 'Invalid session ID'}), 400
    
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    
    # Clear any old notifications
    while not notification_queues[session_id].empty():
        notification_queues[session_id].get()
    
    # Process the query asynchronously
    def process_async():
        # Get or create event loop for this thread
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Store the loop for this session
        event_loops[session_id] = loop
        
        # Process the query
        agent_session = agent_sessions[session_id]
        response = loop.run_until_complete(
            agent_session.orchestrator.process_query(query)
        )
        
        # Add final response to queue
        notification_queues[session_id].put({
            'type': 'final_response',
            'response': response
        })
    
    # Start processing in a separate thread
    thread = Thread(target=process_async)
    thread.start()
    
    return jsonify({'status': 'processing'})

@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    session_id = request.args.get('session_id')
    
    if not session_id or session_id not in notification_queues:
        return jsonify({'error': 'Invalid session ID'}), 400
    
    # Get all available notifications
    notifications = []
    while not notification_queues[session_id].empty():
        notifications.append(notification_queues[session_id].get())
    
    return jsonify({'notifications': notifications})

if __name__ == '__main__':
    # Ensure templates directory exists
    import os
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    app.run(debug=True)
