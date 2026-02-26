"""
Basic Usage Examples for Jarvis Brain
Demonstrates how to use different components of the system.
"""

from core.voice_nlp import VoiceRecognizer, NLPProcessor
from core.reasoning import ReasoningEngine, Task
from core.decision_layer import DecisionLayer, AgentType
from core.security import AuthenticationManager, AuditLogger, RollbackManager
from agents.mac_agent import MacAgent
from agents.android_agent import AndroidAgent
from modules.whatsapp import WhatsAppManager, WhatsAppConnectionMode
from modules.dashboard import Dashboard, AlertManager
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def example_voice_nlp():
    """Example: Voice recognition and NLP processing."""
    print("\n=== Voice & NLP Example ===")
    
    recognizer = VoiceRecognizer()
    processor = NLPProcessor()
    
    # Simulate voice input
    recognizer.start_listening()
    print("🎤 Listening for voice input...")
    
    # Process a command
    command = "send message to john on whatsapp"
    result = processor.parse_command(command)
    print(f"✅ Parsed command: {result}")
    
    recognizer.stop_listening()


def example_task_reasoning():
    """Example: Task planning and reasoning."""
    print("\n=== Task Reasoning Example ===")
    
    reasoning = ReasoningEngine()
    
    # Plan a task
    task = Task(
        id="task_001",
        description="Build and deploy backend service",
        priority=1
    )
    
    # Decompose into subtasks
    subtasks = reasoning.decompose_task(task)
    print(f"✅ Task decomposed into {len(subtasks)} subtasks")


def example_agent_assignment():
    """Example: Task assignment to best agent."""
    print("\n=== Agent Assignment Example ===")
    
    decision_layer = DecisionLayer()
    
    # Assign task based on capabilities
    task_type = "build"
    required_capabilities = ["compiler", "git", "dotnet"]
    
    best_agent = decision_layer.assign_task(task_type, required_capabilities)
    print(f"✅ Task assigned to: {best_agent.value if best_agent else 'No suitable agent'}")
    
    # Update performance after task completion
    decision_layer.update_performance(best_agent, success=True)
    performance = decision_layer.evaluate_agent(best_agent)
    print(f"📊 Updated performance score: {performance:.2f}")


def example_mac_agent():
    """Example: Mac agent operations."""
    print("\n=== Mac Agent Example ===")
    
    mac = MacAgent("macmini.local")
    mac.start()
    
    # Build project
    success = mac.build_project("/path/to/project", build_type="release")
    print(f"✅ Build {'successful' if success else 'failed'}")
    
    # Launch VS Code
    mac.launch_vscode("/path/to/workspace")
    
    # Get system info
    info = mac.get_system_info()
    print(f"✅ System info: {info}")
    
    mac.stop()


def example_android_agent():
    """Example: Android agent operations."""
    print("\n=== Android Agent Example ===")
    
    android = AndroidAgent("emulator-5554")
    android.start()
    
    # Send WhatsApp message
    android.send_whatsapp_message("+1234567890", "Hello from Jarvis!")
    
    # Send SMS
    android.send_sms("+1234567890", "Test SMS")
    
    # Enable hotspot
    android.enable_hotspot()
    
    # Get battery level
    battery = android.get_battery_level()
    print(f"✅ Battery level: {battery}%")
    
    android.stop()


def example_whatsapp_integration():
    """Example: WhatsApp messaging."""
    print("\n=== WhatsApp Integration Example ===")
    
    whatsapp = WhatsAppManager(WhatsAppConnectionMode.WEB)
    whatsapp.connect()
    whatsapp.authenticate({"credentials": "example"})
    
    # Send message
    success = whatsapp.send_message("+1234567890", "Hello from Jarvis!")
    print(f"✅ Message {'sent' if success else 'failed'}")
    
    # Get contact list
    contacts = whatsapp.get_contact_list()
    print(f"✅ Retrieved {len(contacts)} contacts")


def example_security_management():
    """Example: Security and audit logging."""
    print("\n=== Security Management Example ===")
    
    # Setup security managers
    auth_manager = AuthenticationManager()
    log_dir = Path("data/logs")
    audit_logger = AuditLogger(log_dir)
    backup_dir = Path("data/backups")
    rollback_manager = RollbackManager(backup_dir)
    
    # Log security events
    audit_logger.log_failed_access("user123", "invalid_password")
    audit_logger.log_task_execution("task_001", "mac_agent", "success")
    
    # Create snapshot for rollback
    snapshot_id = "snapshot_2026_02_26_001"
    rollback_manager.create_snapshot(snapshot_id)
    print(f"✅ Created snapshot: {snapshot_id}")
    
    # Rollback if needed
    rollback_manager.rollback_to(snapshot_id)
    print(f"✅ Rolled back to: {snapshot_id}")


def example_dashboard_alerts():
    """Example: Dashboard and alerts."""
    print("\n=== Dashboard & Alerts Example ===")
    
    dashboard = Dashboard(port=8080)
    dashboard.start()
    
    alert_manager = AlertManager()
    
    # Add widget
    dashboard.add_widget("cpu_monitor", {"type": "gauge", "value": 75})
    
    # Create alerts
    alert_id = alert_manager.create_alert("high_cpu", "CPU usage exceeded 80%", severity="warning")
    print(f"✅ Created alert: {alert_id}")
    
    # Get active alerts
    active = alert_manager.get_active_alerts()
    print(f"✅ Active alerts: {len(active)}")
    
    dashboard.stop()


def run_all_examples():
    """Run all examples."""
    print("╔════════════════════════════════════════════════════════╗")
    print("║     Jarvis Brain - Basic Usage Examples                ║")
    print("╚════════════════════════════════════════════════════════╝")
    
    try:
        example_voice_nlp()
        example_task_reasoning()
        example_agent_assignment()
        example_mac_agent()
        example_android_agent()
        example_whatsapp_integration()
        example_security_management()
        example_dashboard_alerts()
        
        print("\n✅ All examples completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        logger.exception("Example execution failed")


if __name__ == "__main__":
    run_all_examples()
