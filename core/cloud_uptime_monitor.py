"""
Cloud Uptime Monitor
24/7 cloud node that keeps Jarvis alive when local HQ is offline.
"""

import logging
from typing import Dict, Optional, List
from datetime import datetime, timedelta
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class CloudUptimeMonitor:
    """Monitors Jarvis HQ and acts as backup brain when offline."""
    
    def __init__(self, region: str = "us-east-1"):
        """
        Initialize cloud uptime monitor.
        
        Args:
            region: Cloud region
        """
        self.region = region
        self.is_active = True
        self.hq_status = {
            "online": False,
            "last_heartbeat": None,
            "uptime_seconds": 0
        }
        self.queued_commands: List[Dict] = []
        self.backup_data_path = Path("data/cloud_backup")
        self.backup_data_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Cloud uptime monitor initialized (region: {region})")
    
    def receive_heartbeat(self, hq_status: Dict) -> None:
        """
        Receive heartbeat from local HQ.
        
        Args:
            hq_status: Status data from HQ
        """
        self.hq_status["online"] = True
        self.hq_status["last_heartbeat"] = datetime.now().isoformat()
        logger.info("💓 Heartbeat received from HQ")
    
    def check_hq_health(self, heartbeat_timeout: int = 300) -> bool:
        """
        Check if HQ is still online.
        
        Args:
            heartbeat_timeout: Timeout in seconds
            
        Returns:
            Whether HQ is healthy
        """
        if not self.hq_status["last_heartbeat"]:
            return True  # Never received heartbeat, assume offline is intentional
        
        last_heartbeat = datetime.fromisoformat(self.hq_status["last_heartbeat"])
        if (datetime.now() - last_heartbeat).total_seconds() > heartbeat_timeout:
            self.hq_status["online"] = False
            logger.warning("⚠️ HQ offline detected by watchdog")
            return False
        
        return True
    
    def queue_command(self, command: str, agent_type: str = "cloud", priority: int = 0) -> str:
        """
        Queue command while HQ is offline.
        
        Args:
            command: Command to execute
            agent_type: Target agent type
            priority: Command priority
            
        Returns:
            Command ID
        """
        cmd_id = f"cmd_{len(self.queued_commands)}_{datetime.now().timestamp()}"
        
        queued_cmd = {
            "id": cmd_id,
            "command": command,
            "agent_type": agent_type,
            "priority": priority,
            "queued_at": datetime.now().isoformat(),
            "status": "queued"
        }
        
        self.queued_commands.append(queued_cmd)
        logger.info(f"📋 Command queued: {cmd_id} - {command[:50]}...")
        
        return cmd_id
    
    def execute_queued_commands(self) -> Dict:
        """
        Execute all queued commands now that HQ is back online.
        
        Returns:
            Execution results
        """
        if not self.queued_commands:
            logger.info("No queued commands to execute")
            return {"executed": 0, "failed": 0}
        
        results = {
            "executed": 0,
            "failed": 0,
            "commands": []
        }
        
        # Sort by priority (higher first)
        sorted_commands = sorted(self.queued_commands, key=lambda x: x["priority"], reverse=True)
        
        for cmd in sorted_commands:
            logger.info(f"⚡ Executing queued command: {cmd['id']}")
            
            # In production, these would be routed to actual agents
            # For now, just mark as executed
            cmd["status"] = "executed"
            cmd["executed_at"] = datetime.now().isoformat()
            
            results["executed"] += 1
            results["commands"].append({
                "id": cmd["id"],
                "status": "executed",
                "timestamp": cmd["executed_at"]
            })
        
        self.queued_commands = []
        logger.info(f"✅ Executed {results['executed']} queued commands")
        
        return results
    
    def backup_data(self, data: Dict, backup_type: str = "logs") -> bool:
        """
        Backup data to cloud storage.
        
        Args:
            data: Data to backup
            backup_type: Type of backup (logs, code, config)
            
        Returns:
            Backup success
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self.backup_data_path / f"{backup_type}_{timestamp}.json"
            
            with open(backup_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"✅ Data backed up: {backup_file}")
            return True
        
        except Exception as e:
            logger.error(f"❌ Backup failed: {e}")
            return False
    
    def restore_data(self, backup_type: str = "logs", limit: int = 1) -> List[Dict]:
        """
        Restore data from backup.
        
        Args:
            backup_type: Type of backup to restore
            limit: Maximum backups to restore
            
        Returns:
            Restored data list
        """
        restored_data = []
        
        try:
            backup_files = sorted(
                self.backup_data_path.glob(f"{backup_type}_*.json"),
                reverse=True
            )[:limit]
            
            for backup_file in backup_files:
                with open(backup_file, 'r') as f:
                    data = json.load(f)
                    restored_data.append(data)
                    logger.info(f"✅ Restored: {backup_file}")
        
        except Exception as e:
            logger.error(f"❌ Restore failed: {e}")
        
        return restored_data
    
    def get_cloud_stats(self) -> Dict:
        """
        Get cloud monitor statistics.
        
        Returns:
            Statistics dictionary
        """
        return {
            "region": self.region,
            "is_active": self.is_active,
            "hq_status": self.hq_status,
            "queued_commands": len(self.queued_commands),
            "timestamp": datetime.now().isoformat()
        }
