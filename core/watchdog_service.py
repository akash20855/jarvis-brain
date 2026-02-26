"""
Watchdog Service
Monitors Jarvis HQ and agents, restarts on failure.
"""

import logging
import subprocess
import time
from typing import Dict, Optional
from datetime import datetime
from pathlib import Path
import psutil
import json

logger = logging.getLogger(__name__)


class WatchdogService:
    """Monitors Jarvis HQ and restarts on failure."""
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize watchdog service.
        
        Args:
            config_path: Path to watchdog config
        """
        self.config_path = config_path or Path("configs/watchdog.json")
        self.monitored_services: Dict = {
            "jarvis_hq": {
                "process_name": "jarvis",
                "command": "python3 core/main.py",
                "restart_enabled": True,
                "max_restarts": 5,
                "restart_count": 0
            }
        }
        self.heart_beat_interval = 10  # seconds
        self.is_running = False
        logger.info("Watchdog service initialized")
    
    def start_monitoring(self) -> None:
        """Start monitoring services."""
        logger.info("🔍 Watchdog monitoring started")
        self.is_running = True
        
        while self.is_running:
            for service_name, config in self.monitored_services.items():
                self._check_and_restart_service(service_name, config)
            
            time.sleep(self.heart_beat_interval)
    
    def _check_and_restart_service(self, service_name: str, config: Dict) -> None:
        """
        Check if service is running and restart if needed.
        
        Args:
            service_name: Name of service
            config: Service configuration
        """
        process_name = config.get("process_name")
        
        # Check if process is running
        is_running = self._is_process_running(process_name)
        
        if not is_running and config.get("restart_enabled"):
            logger.warning(f"⚠️ {service_name} is not running. Attempting restart...")
            
            if config["restart_count"] < config.get("max_restarts", 5):
                if self._restart_service(service_name, config):
                    config["restart_count"] += 1
                    logger.info(f"✅ {service_name} restarted (count: {config['restart_count']})")
                else:
                    logger.error(f"❌ Failed to restart {service_name}")
            else:
                logger.error(f"❌ {service_name} exceeded max restarts. Manual intervention needed.")
    
    def _is_process_running(self, process_name: str) -> bool:
        """
        Check if process is running.
        
        Args:
            process_name: Process name to check
            
        Returns:
            Whether process is running
        """
        try:
            for proc in psutil.process_iter(['name']):
                if process_name.lower() in proc.name().lower():
                    return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
        return False
    
    def _restart_service(self, service_name: str, config: Dict) -> bool:
        """
        Restart a service.
        
        Args:
            service_name: Service name
            config: Service configuration
            
        Returns:
            Restart success
        """
        try:
            command = config.get("command")
            logger.info(f"Running: {command}")
            
            subprocess.Popen(command, shell=True)
            time.sleep(2)  # Give service time to start
            
            return self._is_process_running(config.get("process_name"))
        
        except Exception as e:
            logger.error(f"Error restarting service: {e}")
            return False
    
    def get_service_health(self) -> Dict:
        """
        Get health status of monitored services.
        
        Returns:
            Health status dictionary
        """
        health = {
            "timestamp": datetime.now().isoformat(),
            "services": {}
        }
        
        for service_name, config in self.monitored_services.items():
            is_running = self._is_process_running(config.get("process_name"))
            health["services"][service_name] = {
                "running": is_running,
                "restart_count": config.get("restart_count", 0),
                "max_restarts": config.get("max_restarts", 5)
            }
        
        return health
    
    def stop_monitoring(self) -> None:
        """Stop monitoring services."""
        logger.info("🛑 Watchdog monitoring stopped")
        self.is_running = False
