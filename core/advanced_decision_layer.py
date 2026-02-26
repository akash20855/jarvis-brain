"""
Advanced Decision Layer with Machine Learning
Intelligent task assignment based on performance metrics and learning.
"""

import logging
from typing import Dict, List, Optional, Tuple
from enum import Enum
from datetime import datetime, timedelta
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class AgentType(Enum):
    """Available agent types."""
    MAC = "mac"
    WINDOWS = "windows"
    ANDROID = "android"
    CLOUD = "cloud"


class AdvancedDecisionLayer:
    """Advanced AI decision layer with performance learning."""
    
    def __init__(self, metrics_file: Optional[Path] = None):
        """
        Initialize advanced decision layer.
        
        Args:
            metrics_file: Path to save performance metrics
        """
        self.metrics_file = metrics_file or Path("data/metrics/agent_performance.json")
        self.metrics_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Performance tracking
        self.agent_performance: Dict[AgentType, float] = {
            AgentType.MAC: 0.9,
            AgentType.WINDOWS: 0.7,
            AgentType.ANDROID: 0.6,
            AgentType.CLOUD: 0.8,
        }
        
        self.task_history: List[Dict] = []
        self.load_metrics()
        
        logger.info("Advanced decision layer with AI learning initialized")
    
    def load_metrics(self) -> None:
        """Load saved performance metrics."""
        if self.metrics_file.exists():
            try:
                with open(self.metrics_file) as f:
                    data = json.load(f)
                    self.task_history = data.get("task_history", [])
                    for agent_name, score in data.get("agent_performance", {}).items():
                        try:
                            agent_type = AgentType[agent_name.upper()]
                            self.agent_performance[agent_type] = score
                        except KeyError:
                            pass
                logger.info("Performance metrics loaded")
            except Exception as e:
                logger.error(f"Error loading metrics: {e}")
    
    def save_metrics(self) -> None:
        """Save performance metrics to file."""
        try:
            data = {
                "agent_performance": {agent.name.lower(): score for agent, score in self.agent_performance.items()},
                "task_history": self.task_history[-100:],  # Keep last 100 tasks
                "last_saved": datetime.now().isoformat()
            }
            with open(self.metrics_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving metrics: {e}")
    
    def assign_task(self, task_type: str, required_capabilities: List[str], priority: int = 0) -> Optional[AgentType]:
        """
        Intelligently assign task to best agent.
        
        Args:
            task_type: Type of task
            required_capabilities: Required agent capabilities
            priority: Task priority (higher = more urgent)
            
        Returns:
            Assigned agent type
        """
        logger.info(f"Assigning {task_type} task (priority: {priority})")
        
        # Find capable agents
        capable_agents = self._find_capable_agents(required_capabilities)
        
        if not capable_agents:
            logger.warning(f"No capable agents found for {task_type}")
            return None
        
        # Select best agent based on:
        # 1. Performance score
        # 2. Recent success rate
        # 3. Current load
        best_agent = max(
            capable_agents,
            key=lambda a: self._calculate_assignment_score(a, priority)
        )
        
        logger.info(f"✅ Task assigned to: {best_agent.value}")
        
        # Record assignment
        self.task_history.append({
            "timestamp": datetime.now().isoformat(),
            "task_type": task_type,
            "assigned_agent": best_agent.name,
            "status": "pending"
        })
        
        return best_agent
    
    def _find_capable_agents(self, capabilities: List[str]) -> List[AgentType]:
        """
        Find agents with required capabilities.
        
        Args:
            capabilities: Required capabilities
            
        Returns:
            List of capable agents
        """
        capability_map = {
            AgentType.MAC: ["build", "vscode", "render", "coding", "git"],
            AgentType.WINDOWS: ["deploy", "services", "powershell", "dotnet"],
            AgentType.ANDROID: ["messaging", "sms", "hotspot", "notifications"],
            AgentType.CLOUD: ["research", "planning", "monitoring", "scaling", "24h_uptime"],
        }
        
        capable = []
        for agent_type, agent_capabilities in capability_map.items():
            if any(req_cap in agent_capabilities for req_cap in capabilities):
                capable.append(agent_type)
        
        return capable or list(AgentType)
    
    def _calculate_assignment_score(self, agent: AgentType, priority: int = 0) -> float:
        """
        Calculate assignment score for an agent.
        
        Args:
            agent: Agent type
            priority: Task priority
            
        Returns:
            Assignment score
        """
        # Base performance score
        base_score = self.agent_performance.get(agent, 0.5)
        
        # Recent success rate (last 10 tasks)
        recent_tasks = [t for t in self.task_history if t["assigned_agent"] == agent.name][-10:]
        success_rate = sum(1 for t in recent_tasks if t.get("status") == "success") / max(len(recent_tasks), 1)
        
        # Priority bonus
        priority_bonus = priority * 0.01
        
        # Calculate final score
        final_score = (base_score * 0.6) + (success_rate * 0.3) + priority_bonus + 0.1
        
        return final_score
    
    def update_performance(self, agent: AgentType, task_id: str, success: bool, execution_time: float = 0) -> None:
        """
        Update agent performance after task completion.
        
        Args:
            agent: Agent type
            task_id: Task identifier
            success: Whether task was successful
            execution_time: Task execution time in seconds
        """
        # Update overall performance
        current_score = self.agent_performance.get(agent, 0.5)
        
        # Adjust based on success and execution time
        time_bonus = min(execution_time / 3600, 0.1)  # Max 0.1 for fast execution
        delta = (0.05 if success else -0.10) + time_bonus
        
        new_score = max(0.0, min(1.0, current_score + delta))
        self.agent_performance[agent] = new_score
        
        # Update task history
        for task in reversed(self.task_history):
            if task.get("assigned_agent") == agent.name and task.get("status") == "pending":
                task["status"] = "success" if success else "failed"
                task["execution_time"] = execution_time
                break
        
        logger.info(f"Updated {agent.value} performance: {current_score:.2f} → {new_score:.2f}")
        self.save_metrics()
    
    def get_agent_stats(self, agent: Optional[AgentType] = None) -> Dict:
        """
        Get agent statistics.
        
        Args:
            agent: Specific agent or None for all
            
        Returns:
            Agent statistics
        """
        if agent:
            agents = [agent]
        else:
            agents = list(AgentType)
        
        stats = {}
        for agent_type in agents:
            agent_tasks = [t for t in self.task_history if t["assigned_agent"] == agent_type.name]
            
            if agent_tasks:
                successful = sum(1 for t in agent_tasks if t.get("status") == "success")
                avg_time = sum(t.get("execution_time", 0) for t in agent_tasks) / len(agent_tasks)
            else:
                successful = 0
                avg_time = 0
            
            stats[agent_type.name] = {
                "performance_score": self.agent_performance[agent_type],
                "total_tasks": len(agent_tasks),
                "successful_tasks": successful,
                "success_rate": successful / len(agent_tasks) if agent_tasks else 0,
                "avg_execution_time": avg_time
            }
        
        return stats
    
    def get_recommendations(self) -> List[str]:
        """
        Get AI recommendations for optimization.
        
        Returns:
            List of recommendations
        """
        recommendations = []
        
        stats = self.get_agent_stats()
        
        # Check for underperforming agents
        for agent_name, metrics in stats.items():
            if metrics["performance_score"] < 0.5:
                recommendations.append(f"⚠️ {agent_name} is underperforming. Consider maintenance or reassignment.")
        
        # Check for overused agents
        total_tasks = sum(metrics["total_tasks"] for metrics in stats.values())
        for agent_name, metrics in stats.items():
            if metrics["total_tasks"] > total_tasks * 0.6:
                recommendations.append(f"💡 {agent_name} is heavily used. Consider load balancing.")
        
        # High execution times
        for agent_name, metrics in stats.items():
            if metrics["avg_execution_time"] > 300:  # > 5 minutes
                recommendations.append(f"⏱️ {agent_name} has high execution time. Investigate performance issues.")
        
        return recommendations or ["✅ System performing well. No immediate recommendations."]
