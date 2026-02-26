"""
Research Module
Research and planning engine for knowledge gathering and task planning.
"""

import logging
from typing import Optional, Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)


class ResearchEngine:
    """Handles research tasks and knowledge gathering."""
    
    def __init__(self):
        """Initialize research engine."""
        self.knowledge_base: Dict[str, List[str]] = {}
        self.research_tasks: Dict[str, Dict] = {}
        logger.info("Research engine initialized")
    
    def start_research(self, topic: str, query: str) -> str:
        """
        Start research task.
        
        Args:
            topic: Research topic
            query: Research query
            
        Returns:
            Research task ID
        """
        task_id = f"research_{len(self.research_tasks)}"
        self.research_tasks[task_id] = {
            "topic": topic,
            "query": query,
            "status": "running",
            "started_at": datetime.now().isoformat(),
            "results": []
        }
        logger.info(f"Started research task: {task_id} - Topic: {topic}")
        return task_id
    
    def add_source(self, topic: str, source: str) -> None:
        """
        Add source to knowledge base.
        
        Args:
            topic: Topic category
            source: Source information
        """
        if topic not in self.knowledge_base:
            self.knowledge_base[topic] = []
        self.knowledge_base[topic].append(source)
        logger.info(f"Added source to {topic}: {source[:50]}...")
    
    def search_knowledge(self, query: str, topic: Optional[str] = None) -> List[str]:
        """
        Search knowledge base.
        
        Args:
            query: Search query
            topic: Optional topic filter
            
        Returns:
            Matching sources
        """
        logger.info(f"Searching knowledge base for: {query}")
        results = []
        
        if topic and topic in self.knowledge_base:
            results = self.knowledge_base[topic]
        elif not topic:
            for sources in self.knowledge_base.values():
                results.extend(sources)
        
        return results
    
    def get_research_status(self, task_id: str) -> Optional[Dict]:
        """
        Get research task status.
        
        Args:
            task_id: Research task ID
            
        Returns:
            Task status or None
        """
        return self.research_tasks.get(task_id)
    
    def complete_research(self, task_id: str, results: List[str]) -> bool:
        """
        Mark research task complete.
        
        Args:
            task_id: Research task ID
            results: Research results
            
        Returns:
            Success status
        """
        if task_id in self.research_tasks:
            self.research_tasks[task_id]["status"] = "completed"
            self.research_tasks[task_id]["results"] = results
            self.research_tasks[task_id]["completed_at"] = datetime.now().isoformat()
            logger.info(f"Completed research task: {task_id}")
            return True
        return False


class PlanningEngine:
    """Handles planning and strategy development."""
    
    def __init__(self):
        """Initialize planning engine."""
        self.plans: Dict[str, Dict] = {}
        logger.info("Planning engine initialized")
    
    def create_plan(self, objective: str, constraints: Optional[List[str]] = None) -> str:
        """
        Create strategic plan.
        
        Args:
            objective: Plan objective
            constraints: Optional constraints
            
        Returns:
            Plan ID
        """
        plan_id = f"plan_{len(self.plans)}"
        self.plans[plan_id] = {
            "objective": objective,
            "constraints": constraints or [],
            "steps": [],
            "created_at": datetime.now().isoformat(),
            "status": "draft"
        }
        logger.info(f"Created plan: {plan_id} - Objective: {objective}")
        return plan_id
    
    def add_step(self, plan_id: str, step: Dict) -> bool:
        """
        Add step to plan.
        
        Args:
            plan_id: Plan ID
            step: Step information
            
        Returns:
            Success status
        """
        if plan_id not in self.plans:
            return False
        
        self.plans[plan_id]["steps"].append(step)
        logger.info(f"Added step to plan {plan_id}: {step.get('description', '')}")
        return True
    
    def finalize_plan(self, plan_id: str) -> bool:
        """
        Finalize plan.
        
        Args:
            plan_id: Plan ID
            
        Returns:
            Success status
        """
        if plan_id not in self.plans:
            return False
        
        self.plans[plan_id]["status"] = "finalized"
        self.plans[plan_id]["finalized_at"] = datetime.now().isoformat()
        logger.info(f"Finalized plan: {plan_id}")
        return True
    
    def get_plan(self, plan_id: str) -> Optional[Dict]:
        """
        Get plan details.
        
        Args:
            plan_id: Plan ID
            
        Returns:
            Plan details or None
        """
        return self.plans.get(plan_id)
