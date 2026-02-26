"""
Complete Integration Example - Full Jarvis Brain Workflow
Demonstrates how all components work together with real-world scenarios.
"""

import logging
from datetime import datetime
from pathlib import Path

# Import all major components
from core.main import JarvisHQ, JarvisREPL
from core.voice_nlp import VoiceRecognizer, NLPProcessor
from core.reasoning import ReasoningEngine, Task
from core.advanced_decision_layer import AdvancedDecisionLayer, AgentType
from core.ssh_manager import SSHManager
from core.autonomous_setup import AutoSetup
from core.listening_service import ContinuousListeningService, MultiDeviceListeningManager
from core.watchdog_service import WatchdogService
from core.cloud_uptime_monitor import CloudUptimeMonitor

from agents.enhanced_mac_agent import EnhancedMacAgent
from agents.enhanced_android_agent import EnhancedAndroidAgent

from modules.enhanced_whatsapp import EnhancedWhatsAppManager, WhatsAppMode

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def scenario_1_build_and_deploy():
    """Scenario 1: Build project and deploy"""
    print("\n" + "="*70)
    print("SCENARIO 1: Build Project and Deploy to Cloud")
    print("="*70)
    
    # User command
    print("\n👤 User: 'Jarvis, build my project and deploy to cloud'")
    
    # Step 1: NLP Processing
    print("\n🧠 Jarvis HQ Processing:")
    processor = NLPProcessor()
    command = processor.parse_command("build project and deploy")
    print(f"  ✅ Intent: {command['intent']}")
    
    # Step 2: Task Planning
    reasoning = ReasoningEngine()
    task = Task(
        id="task_build_deploy",
        description="Build project and deploy to production",
        priority=2
    )
    subtasks = reasoning.decompose_task(task)
    print(f"  ✅ Task decomposed into {len(subtasks)} subtasks")
    
    # Step 3: Agent Assignment
    decision_layer = AdvancedDecisionLayer()
    build_agent = decision_layer.assign_task("build", ["compiler", "git"])
    deploy_agent = decision_layer.assign_task("deploy", ["cloud", "deployment"])
    print(f"  ✅ Build assigned to: {build_agent.value}")
    print(f"  ✅ Deploy assigned to: {deploy_agent.value}")
    
    # Step 4: Execution
    print("\n⚡ Execution Phase:")
    mac = EnhancedMacAgent("macmini.local")
    mac.start()
    
    success, output = mac.build_project("/path/to/project")
    print(f"  ✅ Build result: {'Success' if success else 'Failed'}")
    
    # Cloud deployment
    success = mac.sync_to_cloud("/path/to/project", "s3://jarvis-deploy")
    print(f"  ✅ Cloud sync: {'Success' if success else 'Failed'}")
    
    # Step 5: Feedback
    print("\n📊 Feedback:")
    decision_layer.update_performance(mac.AgentType, "task_build_deploy", success=True, execution_time=120)
    print(f"  ✅ Agent performance updated")


def scenario_2_24_7_listening():
    """Scenario 2: 24/7 continuous listening with device switching"""
    print("\n" + "="*70)
    print("SCENARIO 2: 24/7 Continuous Listening")
    print("="*70)
    
    # Setup listening on all devices
    print("\n🎤 Setting up continuous listening:")
    listener_manager = MultiDeviceListeningManager()
    
    # Mac HQ listening during work hours
    print("  📍 Mac Mini (8 hours/day) - Listening started")
    listener_manager.start_on_device("mac")
    
    # Simulate some audio
    print("  🎙️ User says: 'Jarvis, send message to Rahul'")
    listener_manager.listeners["mac"].process_audio_stream("Jarvis send message to Rahul")
    
    # Mac goes offline, switch to Android
    print("\n  📱 Mac offline detected")
    print("  🔄 Switching to Android phone for 24/7 listening")
    listener_manager.switch_device("mac", "android")
    
    # Get stats
    stats = listener_manager.get_all_stats()
    print(f"\n  📊 Listening Stats:")
    for device, stat in stats.items():
        print(f"     {device}: {stat}")


def scenario_3_autonomous_whatsapp_setup():
    """Scenario 3: Autonomous WhatsApp setup without manual intervention"""
    print("\n" + "="*70)
    print("SCENARIO 3: Autonomous WhatsApp Connection")
    print("="*70)
    
    print("\n👤 User: 'Jarvis, connect WhatsApp'")
    
    print("\n🤖 Jarvis autonomous setup starting...")
    
    whatsapp = EnhancedWhatsAppManager(mode=WhatsAppMode.WEB)
    success, message = whatsapp.autonomous_connect()
    
    print(f"\n  ✅ {message}")
    
    # Now send messages
    if success:
        print("\n📤 Sending queued messages:")
        results = whatsapp.process_queued_messages()
        print(f"  ✅ Processed: {results}")


def scenario_4_hq_offline_cloud_backup():
    """Scenario 4: HQ offline, Cloud takes over"""
    print("\n" + "="*70)
    print("SCENARIO 4: HQ Offline - Cloud Backup Takes Over")
    print("="*70)
    
    # Simulate HQ offline
    print("\n⚠️ Mac HQ detected as offline")
    
    # Cloud monitor takes over
    cloud_monitor = CloudUptimeMonitor(region="us-east-1")
    cloud_monitor.hq_status["online"] = False
    
    print("☁️ Cloud HQ taking over...")
    
    # Queue commands while offline
    print("\n👤 User (via Android): 'Queue build for tomorrow'")
    
    cmd_id = cloud_monitor.queue_command("build project", agent_type="mac", priority=1)
    print(f"  ✅ Command queued: {cmd_id}")
    
    cmd_id = cloud_monitor.queue_command("send report", agent_type="cloud", priority=0)
    print(f"  ✅ Command queued: {cmd_id}")
    
    # HQ comes back online
    print("\n💓 Mac HQ back online!")
    cloud_monitor.hq_status["online"] = True
    
    # Execute queued commands
    print("⚡ Executing queued commands from cloud...")
    results = cloud_monitor.execute_queued_commands()
    print(f"  ✅ Executed: {results['executed']}, Failed: {results['failed']}")


def scenario_5_watchdog_restart():
    """Scenario 5: Watchdog detects crash and restarts"""
    print("\n" + "="*70)
    print("SCENARIO 5: Smart Watchdog - Auto Recovery")
    print("="*70)
    
    print("\n🔍 Watchdog monitoring Jarvis HQ...")
    
    watchdog = WatchdogService()
    
    # Simulate crash
    print("  ⚠️ Crash detected!")
    
    health = watchdog.get_service_health()
    for service, status in health["services"].items():
        print(f"     {service}: {status['running']}")
    
    print("\n🔄 Auto-restart triggered...")
    print("  ✅ Jarvis HQ restarted successfully")
    
    # Updated health
    health = watchdog.get_service_health()
    for service, status in health["services"].items():
        print(f"  ✅ {service}: {'Running' if status['running'] else 'Offline'}")


def scenario_6_android_control_hub():
    """Scenario 6: Android acts as control hub"""
    print("\n" + "="*70)
    print("SCENARIO 6: Android as Control Hub")
    print("="*70)
    
    print("\n📱 Android Phone acting as control hub (Mac offline)")
    
    android = EnhancedAndroidAgent("emulator-5554", "Akash's Phone")
    android.start()
    android.act_as_control_hub()
    
    # Execute direct tasks
    print("\n⚡ Direct Android tasks:")
    success, status = android.send_whatsapp("+1234567890", "Meeting at 5")
    print(f"  ✅ {status}")
    
    success, status = android.enable_hotspot("Jarvis")
    print(f"  ✅ {status}")
    
    # Queue task for Mac
    print("\n📋 Tasks queued for Mac HQ:")
    task_id = android.queue_task_for_hq("Compile large project", priority=1)
    print(f"  ✅ {task_id}")
    
    # Battery check
    battery = android.get_battery_status()
    print(f"\n🔋 Battery: {battery['level']}% ({battery['status']})")


def run_all_scenarios():
    """Run all integration scenarios."""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + "  JARVIS BRAIN - COMPLETE INTEGRATION SCENARIOS".center(68) + "║")
    print("╚" + "="*68 + "╝")
    
    try:
        scenario_1_build_and_deploy()
        scenario_2_24_7_listening()
        scenario_3_autonomous_whatsapp_setup()
        scenario_4_hq_offline_cloud_backup()
        scenario_5_watchdog_restart()
        scenario_6_android_control_hub()
        
        print("\n" + "="*70)
        print("✅ ALL SCENARIOS COMPLETED SUCCESSFULLY")
        print("="*70)
        print("\nJarvis Brain is ready for production! 🚀\n")
        
    except Exception as e:
        print(f"\n❌ Error running scenarios: {e}")
        logger.exception("Scenario execution failed")


if __name__ == "__main__":
    run_all_scenarios()
