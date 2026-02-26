"""
Jarvis Brain - Intelligent Home Automation and Multi-Device Orchestration
"""

__version__ = "0.1.0"
__author__ = "Jarvis Development Team"

from core import (
    JarvisHQ,
    VoiceRecognizer,
    NLPProcessor,
    ReasoningEngine,
    DecisionLayer,
    AuthenticationManager,
    AuditLogger,
    RollbackManager,
    CloudSync,
    BackupManager,
)

from agents import (
    MacAgent,
    WindowsAgent,
    AndroidAgent,
    CloudAgent,
)

from modules import (
    WhatsAppManager,
    SMSManager,
    HotspotManager,
    NotificationManager,
    Dashboard,
    AlertManager,
    ResearchEngine as ResearchModule,
    PlanningEngine,
)

__all__ = [
    # Core
    'JarvisHQ',
    'VoiceRecognizer',
    'NLPProcessor',
    'ReasoningEngine',
    'DecisionLayer',
    'AuthenticationManager',
    'AuditLogger',
    'RollbackManager',
    'CloudSync',
    'BackupManager',
    # Agents
    'MacAgent',
    'WindowsAgent',
    'AndroidAgent',
    'CloudAgent',
    # Modules
    'WhatsAppManager',
    'SMSManager',
    'HotspotManager',
    'NotificationManager',
    'Dashboard',
    'AlertManager',
    'ResearchModule',
    'PlanningEngine',
]
