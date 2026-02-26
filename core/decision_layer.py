"""
Decision Layer - IQ Module (Performance-based Assignment)
Determines the best agent for task execution based on performance metrics and capabilities.
"""

import logging
from typing import Dict, Optional, List
from enum import Enum

logger = logging.getLogger(__name__)


class AgentType(Enum):
    """Available agent types."""
    MAC = "mac"
    WINDOWS = "windows"
    ANDROID = "android"
    CLOUD = "cloud"


class DecisionLayer:
    """Intelligent decision making for task assignment."""
    
    def __init__(self):
        """Initialize decision layer."""
        self.agent_performance: Dict[AgentType, float] = {
            AgentType.MAC: 0.9,
            AgentType.WINDOWS: 0.8,
            AgentType.ANDROID: 0.7,
            AgentType.CLOUD: 0.85,
        }
        logger.info("Decision layer initialized")
    
    def evaluate_agent(self, agent_type: AgentType) -> float:
        """
        Evaluate agent performance score.
        
        Args:
            agent_type: Type of agent
            
        Returns:
            Performance score (0-1)
        """
        return self.agent_performance.get(agent_type, 0.0)
    
    def assign_task(self, task_type: str, required_capabilities: List[str]) -> Optional[AgentType]:
        """
        Assign task to best-suited agent based on performance and capabilities.
        
        Args:
            task_type: Type of task
            required_capabilities: Required agent capabilities
            
        Returns:
            Assigned agent type
        """
        logger.info(f"Assigning task type: {task_type}")
        
        # Placeholder for capability matching and assignment logic
        suitable_agents = self._find_capable_agents(required_capabilities)
        
        if not suitable_agents:
            logger.warning(f"No suitable agent found for task: {task_type}")
            return None
        
        # Select agent with highest performance
        best_agent = max(suitable_agents, key=lambda a: self.evaluate_agent(a))
        logger.info(f"Task assigned to: {best_agent.value}")
        return best_agent
    
    def _find_capable_agents(self, capabilities: List[str]) -> List[AgentType]:
        """
        Find agents with required capabilities.
        
        Args:
            capabilities: Required capabilities
            
        Returns:
            List of capable agents
        """
        # Placeholder for capability matching
        return list(AgentType)
    
    def update_performance(self, agent_type: AgentType, success: bool):
        """
        Update agent performance based on task outcome.
        
        Args:
            agent_type: Agent type
            success: Whether task was successful
        """
        current = self.agent_performance[agent_type]
        # Simple update: +0.02 on success, -0.05 on failure
        delta = 0.02 if success else -0.05
        self.agent_performance[agent_type] = max(0.0, min(1.0, current + delta))
        logger.info(f"Updated {agent_type.value} performance to {self.agent_performance[agent_type]:.2f}")
