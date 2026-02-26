"""
Dashboard Module
Web UI and proactive alerts system.
"""

import logging
from typing import Optional, Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)


class Dashboard:
    """Dashboard web interface."""
    
    def __init__(self, port: int = 8080):
        """
        Initialize dashboard.
        
        Args:
            port: Port number for dashboard
        """
        self.port = port
        self.is_running = False
        self.widgets: Dict[str, Dict] = {}
        logger.info(f"Dashboard initialized on port {port}")
    
    def start(self) -> bool:
        """Start dashboard server."""
        logger.info(f"Starting dashboard on port {self.port}")
        self.is_running = True
        return True
    
    def stop(self) -> bool:
        """Stop dashboard server."""
        logger.info("Stopping dashboard")
        self.is_running = False
        return True
    
    def add_widget(self, widget_id: str, config: Dict) -> bool:
        """
        Add dashboard widget.
        
        Args:
            widget_id: Unique widget identifier
            config: Widget configuration
            
        Returns:
            Success status
        """
        logger.info(f"Adding dashboard widget: {widget_id}")
        self.widgets[widget_id] = config
        return True
    
    def remove_widget(self, widget_id: str) -> bool:
        """
        Remove dashboard widget.
        
        Args:
            widget_id: Widget identifier
            
        Returns:
            Success status
        """
        if widget_id in self.widgets:
            del self.widgets[widget_id]
            logger.info(f"Removed widget: {widget_id}")
            return True
        return False
    
    def get_dashboard_data(self) -> Dict:
        """
        Get current dashboard data.
        
        Returns:
            Dashboard data
        """
        return {
            "widgets": self.widgets,
            "timestamp": datetime.now().isoformat(),
        }


class AlertManager:
    """Manages proactive alerts."""
    
    def __init__(self):
        """Initialize alert manager."""
        self.alerts: List[Dict] = []
        self.alert_handlers: Dict[str, callable] = {}
        logger.info("Alert manager initialized")
    
    def create_alert(self, alert_type: str, message: str, severity: str = "info") -> str:
        """
        Create alert.
        
        Args:
            alert_type: Type of alert
            message: Alert message
            severity: Severity level (info/warning/critical)
            
        Returns:
            Alert ID
        """
        alert_id = f"alert_{len(self.alerts)}"
        alert = {
            "id": alert_id,
            "type": alert_type,
            "message": message,
            "severity": severity,
            "timestamp": datetime.now().isoformat(),
        }
        self.alerts.append(alert)
        logger.info(f"Created alert [{severity}]: {message}")
        return alert_id
    
    def dismiss_alert(self, alert_id: str) -> bool:
        """
        Dismiss alert.
        
        Args:
            alert_id: Alert identifier
            
        Returns:
            Success status
        """
        self.alerts = [a for a in self.alerts if a["id"] != alert_id]
        logger.info(f"Dismissed alert: {alert_id}")
        return True
    
    def register_handler(self, alert_type: str, handler: callable) -> None:
        """
        Register alert handler.
        
        Args:
            alert_type: Alert type to handle
            handler: Handler function
        """
        self.alert_handlers[alert_type] = handler
        logger.info(f"Registered handler for alert type: {alert_type}")
    
    def get_active_alerts(self) -> List[Dict]:
        """
        Get active alerts.
        
        Returns:
            List of active alerts
        """
        return self.alerts.copy()
