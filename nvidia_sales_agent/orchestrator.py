import asyncio
import datetime
import json
from typing import Dict, List, Any
from .claude_helper import ClaudeClient

class OrchestratorAgent:
    """
    Central coordinator that analyzes queries, selects appropriate agents,
    and combines responses from multiple ProductCatalogAgents.
    """
    
    def __init__(self, ui_notifier, claude_client=None):
        """
        Initialize the OrchestratorAgent with a UI notifier for real-time feedback.
        
        Args:
            ui_notifier: An object that handles UI notifications
            claude_client: Optional Claude client for API calls
        """
        self.ui_notifier = ui_notifier
        self.agents = {}
        self.claude_client = claude_client or ClaudeClient()
        
    def register_agent(self, agent_id: str, agent):
        """
        Register a ProductCatalogAgent with the orchestrator.
        
        Args:
            agent_id: Unique identifier for the agent
            agent: The ProductCatalogAgent instance
        """
        self.agents[agent_id] = agent
        
    async def process_query(self, query: str) -> str:
        """
        Process a user query by selecting appropriate agents and combining responses.
        
        Args:
            query: The user's query string
            
        Returns:
            str: The combined response from all relevant agents
        """
        # Notify UI that orchestrator is analyzing query
        self._notify_orchestrator_thinking("Analyzing query to determine relevant product domains...")
        
        # Select agents based on query content using Claude
        selected_agent_ids = await self._select_agents_with_claude(query)
        
        # Notify about agent selection
        agent_list = ", ".join(selected_agent_ids)
        self._notify_orchestrator_thinking(f"Selected agents: {agent_list}")
        
        # Invoke selected agents in parallel
        tasks = []
        for agent_id in selected_agent_ids:
            agent = self.agents[agent_id]
            # Notify UI about agent invocation
            self._notify_agent_invocation(agent_id)
            # Create task for each agent
            tasks.append(self._invoke_agent(agent_id, agent, query))
            
        # Wait for all agent responses
        agent_responses = await asyncio.gather(*tasks)
        
        # Assess if the information is sufficient
        is_sufficient, missing_info = await self._assess_response_sufficiency(query, agent_responses)
        
        if not is_sufficient:
            # Notify UI about insufficient information
            self._notify_orchestrator_thinking(f"The current information is insufficient: {missing_info}. Consulting additional agents...")
            
            # Determine additional agents to query
            additional_agents = await self._select_additional_agents(query, agent_responses, selected_agent_ids, missing_info)
            
            if additional_agents:
                # Notify about additional agents
                agent_list = ", ".join(additional_agents)
                self._notify_orchestrator_thinking(f"Consulting additional agents: {agent_list}")
                
                # Invoke additional agents
                add_tasks = []
                for agent_id in additional_agents:
                    agent = self.agents[agent_id]
                    # Notify UI about agent invocation
                    self._notify_agent_invocation(agent_id)
                    # Create task for each agent
                    add_tasks.append(self._invoke_agent(agent_id, agent, query))
                
                # Wait for additional agent responses
                additional_responses = await asyncio.gather(*add_tasks)
                
                # Add additional responses
                agent_responses.extend(additional_responses)
            
        # Combine responses using Claude
        combined_response = await self._combine_responses_with_claude(query, agent_responses)
        
        return combined_response
        
    async def _invoke_agent(self, agent_id: str, agent, query: str) -> Dict[str, Any]:
        """
        Invoke a single agent and process its response.
        
        Args:
            agent_id: The agent's identifier
            agent: The agent instance
            query: The user query
            
        Returns:
            dict: The agent's response with metadata
        """
        try:
            # Get response from agent
            response = await agent.process_query(query)
            
            # Notify UI about successful completion
            self._notify_agent_completion(agent_id, "completed")
            
            return {
                "agent_id": agent_id,
                "response": response["response"],
                "confidence": response["confidence"],
                "status": "success"
            }
        except Exception as e:
            # Notify UI about failure
            self._notify_agent_completion(agent_id, "failed")
            
            return {
                "agent_id": agent_id,
                "response": f"Error: {str(e)}",
                "confidence": 0.0,
                "status": "error"
            }
            
    async def _select_agents_with_claude(self, query: str) -> List[str]:
        """
        Use Claude to select appropriate agents based on the query content.
        
        Args:
            query: The user query
            
        Returns:
            list: List of agent IDs to invoke
        """
        try:
            # Get available agent IDs
            available_agents = list(self.agents.keys())
            
            # Use Claude to analyze which agents would be appropriate for this query
            system_prompt = """You are an NVIDIA product advisor.
Your job is to determine which specialized NVIDIA product domain agents should be consulted to answer a query.
Select only the agents that are directly relevant to the query."""
            
            prompt = f"""Here is a user query about NVIDIA products:
"{query}"

Available product domain agents:
{', '.join(available_agents)}

Task: Select 1-3 most relevant product domain agents to answer this query.
Return a JSON object with a 'selected_domains' key containing an array of domain names.
"""
            
            response_text = await self.claude_client.get_completion(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.2,
                max_tokens=1024
            )
            
            # Extract the JSON response
            try:
                # Find JSON in the response
                json_start = response_text.find('{')
                json_end = response_text.rfind('}')
                
                if json_start != -1 and json_end != -1:
                    json_str = response_text[json_start:json_end+1]
                    analysis = json.loads(json_str)
                    
                    if 'selected_domains' in analysis and analysis['selected_domains']:
                        # Ensure selected agents exist in our list of agents
                        selected_agents = [agent for agent in analysis['selected_domains'] if agent in self.agents]
                        
                        # If no valid agents found, select up to three available agents
                        if not selected_agents:
                            selected_agents = list(self.agents.keys())[:min(3, len(self.agents))]
                        
                        return selected_agents
                
                # Fallback if JSON parsing fails or selected_domains is empty
                return list(self.agents.keys())[:min(3, len(self.agents))]
                
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                return list(self.agents.keys())[:min(3, len(self.agents))]
                
        except Exception as e:
            print(f"Error in agent selection with Claude: {e}")
            # Fallback - select up to three agents
            return list(self.agents.keys())[:min(3, len(self.agents))]
    
    async def _assess_response_sufficiency(self, query: str, responses: List[Dict]) -> tuple:
        """
        Assess if the information from agents is sufficient to answer the query.
        
        Args:
            query: The original query
            responses: List of agent responses
            
        Returns:
            tuple: (is_sufficient, missing_information)
        """
        try:
            # Filter responses with unsuccessful status
            valid_responses = [r for r in responses if r["status"] == "success"]
            
            if not valid_responses:
                return False, "No valid agent responses received"
                
            # Format responses for Claude to assess
            responses_text = ""
            for i, resp in enumerate(valid_responses):
                responses_text += f"\n--- Information from {resp['agent_id']} ---\n"
                responses_text += resp["response"] + "\n\n"
                
            # Use Claude to assess if information is sufficient
            system_prompt = """You are an NVIDIA product information specialist.
Your task is to assess if the provided information is sufficient to answer a user's query.
Be critical and identify specific missing information that would be needed to provide a complete answer."""

            prompt = f"""User query about NVIDIA products: "{query}"

Information gathered from NVIDIA product domain agents:
{responses_text}

Task: Assess if this information is sufficient to answer the user's query.
Return a JSON object with the following format:
{{
  "is_sufficient": true/false,
  "missing_information": "Description of what information is missing (if any)"
}}

Only return false if critical information needed to answer the query is missing.
If the information is sufficient, even if not comprehensive, return true.
"""

            assessment_text = await self.claude_client.get_completion(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.3,
                max_tokens=800
            )
            
            # Extract the JSON response
            try:
                # Find JSON in the response
                json_start = assessment_text.find('{')
                json_end = assessment_text.rfind('}')
                
                if json_start != -1 and json_end != -1:
                    json_str = assessment_text[json_start:json_end+1]
                    assessment = json.loads(json_str)
                    
                    if 'is_sufficient' in assessment and 'missing_information' in assessment:
                        return assessment['is_sufficient'], assessment['missing_information']
                
                # Fallback if JSON parsing fails
                return True, ""
                
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                return True, ""
                
        except Exception as e:
            print(f"Error in assessing response sufficiency: {e}")
            # Fallback - assume information is sufficient
            return True, ""
    
    async def _select_additional_agents(self, query: str, responses: List[Dict], selected_agents: List[str], missing_info: str) -> List[str]:
        """
        Select additional agents to consult based on missing information.
        
        Args:
            query: The original query
            responses: Current agent responses
            selected_agents: Already selected agents
            missing_info: Description of missing information
            
        Returns:
            list: Additional agent IDs to consult
        """
        try:
            # Get agents that haven't been selected yet
            remaining_agents = [agent for agent in self.agents.keys() if agent not in selected_agents]
            
            if not remaining_agents:
                return []  # No more agents available
                
            # Format existing responses for Claude
            responses_text = ""
            for resp in responses:
                responses_text += f"\n--- Response from {resp['agent_id']} ---\n"
                responses_text += resp["response"][:200] + "...\n\n"
                
            # Use Claude to select additional agents
            system_prompt = """You are an NVIDIA product advisor.
Your job is to determine which additional product domain agents should be consulted to fill gaps in information."""
            
            prompt = f"""User query about NVIDIA products: "{query}"

Current information from agents:
{responses_text}

Missing information identified: {missing_info}

Remaining available agents that haven't been consulted:
{', '.join(remaining_agents)}

Task: Select up to 2 additional agents that are most likely to provide the missing information.
Return a JSON object with a 'selected_domains' key containing an array of domain names.
If no additional agents would be helpful, return an empty array.
"""
            
            response_text = await self.claude_client.get_completion(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.2,
                max_tokens=1024
            )
            
            # Extract the JSON response
            try:
                # Find JSON in the response
                json_start = response_text.find('{')
                json_end = response_text.rfind('}')
                
                if json_start != -1 and json_end != -1:
                    json_str = response_text[json_start:json_end+1]
                    analysis = json.loads(json_str)
                    
                    if 'selected_domains' in analysis:
                        # Ensure selected agents exist in our list and weren't already selected
                        additional_agents = [agent for agent in analysis['selected_domains'] 
                                            if agent in remaining_agents]
                        return additional_agents
                
                # Fallback if JSON parsing fails
                return []
                
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                return []
                
        except Exception as e:
            print(f"Error in selecting additional agents: {e}")
            # Fallback - don't select any additional agents
            return []
    
    async def _combine_responses_with_claude(self, query: str, responses: List[Dict]) -> str:
        """
        Use Claude to combine responses from multiple agents into a coherent answer.
        
        Args:
            query: The original query
            responses: List of agent responses
            
        Returns:
            str: Combined response
        """
        try:
            # Filter responses with unsuccessful status
            valid_responses = [r for r in responses if r["status"] == "success"]
            
            if not valid_responses:
                return "I'm sorry, I couldn't find information to answer your question about NVIDIA products."
                
            # Format responses for Claude to combine
            responses_text = ""
            for i, resp in enumerate(valid_responses):
                responses_text += f"\n--- Information from {resp['agent_id']} ---\n"
                responses_text += resp["response"] + "\n\n"
                
            # Use Claude to generate a combined response
            system_prompt = """You are an NVIDIA product information specialist.
Use ONLY the information provided to answer the query.
Do NOT add any information beyond what's provided in the agent responses.
Be honest about limitations if the provided information is insufficient."""

            prompt = f"""User query about NVIDIA products: "{query}"

Information from various product domain agents:
{responses_text}

Task: Combine this information into a single, coherent answer that directly addresses the user's query.
Only use the information given - do not make up additional specifications or details.
If the information provided doesn't fully answer the query, be upfront about these limitations.
"""

            combined_response = await self.claude_client.get_completion(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.3,
                max_tokens=800
            )
            
            return combined_response
            
        except Exception as e:
            print(f"Error in combining responses with Claude: {e}")
            
            # Fall back to concatenating responses
            responses_text = "Here's what I know about NVIDIA products related to your query:\n\n"
            
            for resp in valid_responses:
                responses_text += f"From {resp['agent_id']}:\n{resp['response']}\n\n"
                
            return responses_text
    
    def _notify_agent_invocation(self, agent_id: str):
        """Notify UI about agent invocation"""
        self.ui_notifier.notify({
            "type": "agent_invocation",
            "agent_id": agent_id,
            "message": f"Consulting {agent_id} agent",
            "timestamp": datetime.datetime.now().isoformat()
        })
    
    def _notify_agent_completion(self, agent_id: str, status: str):
        """Notify UI about agent completion"""
        self.ui_notifier.notify({
            "type": "agent_completion",
            "agent_id": agent_id,
            "message": f"{agent_id} agent finished processing",
            "status": status,
            "timestamp": datetime.datetime.now().isoformat()
        })
    
    def _notify_orchestrator_thinking(self, message: str):
        """Notify UI about orchestrator's thinking process"""
        self.ui_notifier.notify({
            "type": "orchestrator_thinking",
            "message": message,
            "timestamp": datetime.datetime.now().isoformat()
        }) 