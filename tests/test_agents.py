"""
Agents Module Tests
Unit tests for device agents.
"""

import unittest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.mac_agent import MacAgent
from agents.windows_agent import WindowsAgent
from agents.android_agent import AndroidAgent
from agents.cloud_agent import CloudAgent
from agents.enhanced_android_agent import EnhancedAndroidAgent


class TestMacAgent(unittest.TestCase):
    """Test Mac agent functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent = MacAgent()
    
    def test_start_agent(self):
        """Test agent activation."""
        result = self.agent.start()
        self.assertTrue(result)
        self.assertTrue(self.agent.is_active)
    
    def test_stop_agent(self):
        """Test agent deactivation."""
        self.agent.start()
        result = self.agent.stop()
        self.assertTrue(result)
        self.assertFalse(self.agent.is_active)


class TestAndroidAgent(unittest.TestCase):
    """Test Android agent functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent = AndroidAgent("test_device")
    
    def test_start_agent(self):
        """Test agent activation."""
        result = self.agent.start()
        self.assertTrue(result)
        self.assertTrue(self.agent.is_active)

    def test_stop_agent(self):
        """Test agent deactivation."""
        self.agent.start()
        result = self.agent.stop()
        self.assertTrue(result)
        self.assertFalse(self.agent.is_active)

    def test_send_sms(self):
        """Test SMS sending."""
        self.agent.start()
        result = self.agent.send_sms("+1234567890", "Test message")
        self.assertTrue(result)

    def test_send_whatsapp_message(self):
        """Test WhatsApp message sending."""
        self.agent.start()
        result = self.agent.send_whatsapp_message("+1234567890", "Hello via WhatsApp")
        self.assertTrue(result)

    def test_enable_hotspot(self):
        """Test enabling mobile hotspot."""
        self.agent.start()
        result = self.agent.enable_hotspot()
        self.assertTrue(result)

    def test_disable_hotspot(self):
        """Test disabling mobile hotspot."""
        self.agent.start()
        result = self.agent.disable_hotspot()
        self.assertTrue(result)

    def test_get_battery_level(self):
        """Test battery level retrieval."""
        self.agent.start()
        level = self.agent.get_battery_level()
        self.assertIsInstance(level, int)
        self.assertGreaterEqual(level, 0)
        self.assertLessEqual(level, 100)

    def test_send_notification(self):
        """Test push notification sending."""
        self.agent.start()
        result = self.agent.send_notification("Test Title", "Test Message")
        self.assertTrue(result)

    def test_get_device_info(self):
        """Test device information retrieval."""
        info = self.agent.get_device_info()
        self.assertIn("device_id", info)
        self.assertIn("os", info)
        self.assertEqual(info["device_id"], "test_device")
        self.assertEqual(info["os"], "Android")


class TestEnhancedAndroidAgent(unittest.TestCase):
    """Test enhanced Android agent functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.agent = EnhancedAndroidAgent("test_enhanced_device", "Test Phone")

    def test_start_agent(self):
        """Test agent activation."""
        result = self.agent.start()
        self.assertTrue(result)
        self.assertTrue(self.agent.is_active)

    def test_stop_agent(self):
        """Test agent deactivation."""
        self.agent.start()
        result = self.agent.stop()
        self.assertTrue(result)
        self.assertFalse(self.agent.is_active)

    def test_send_whatsapp(self):
        """Test WhatsApp message sending."""
        self.agent.start()
        success, status = self.agent.send_whatsapp("+1234567890", "Hello")
        self.assertTrue(success)
        self.assertIn("+1234567890", status)

    def test_send_sms(self):
        """Test SMS sending."""
        self.agent.start()
        success, status = self.agent.send_sms("+1234567890", "Test SMS")
        self.assertTrue(success)
        self.assertIn("+1234567890", status)

    def test_enable_hotspot(self):
        """Test enabling mobile hotspot."""
        self.agent.start()
        success, status = self.agent.enable_hotspot()
        self.assertTrue(success)
        self.assertTrue(self.agent.hotspot_enabled)

    def test_enable_hotspot_with_ssid(self):
        """Test enabling hotspot with custom SSID."""
        self.agent.start()
        success, status = self.agent.enable_hotspot(ssid="MyNetwork")
        self.assertTrue(success)
        self.assertIn("MyNetwork", status)

    def test_disable_hotspot(self):
        """Test disabling mobile hotspot."""
        self.agent.start()
        self.agent.enable_hotspot()
        success, status = self.agent.disable_hotspot()
        self.assertTrue(success)
        self.assertFalse(self.agent.hotspot_enabled)

    def test_get_battery_status(self):
        """Test battery status retrieval."""
        status = self.agent.get_battery_status()
        self.assertIn("level", status)
        self.assertIn("is_charging", status)
        self.assertIn("status", status)
        self.assertIn(status["status"], ["critical", "low", "good"])

    def test_send_notification(self):
        """Test push notification sending."""
        self.agent.start()
        success, status = self.agent.send_notification("Alert", "Test alert message")
        self.assertTrue(success)
        self.assertIn("Alert", status)

    def test_queue_task_for_hq(self):
        """Test task queuing for Mac HQ."""
        task_id = self.agent.queue_task_for_hq("Run backup", priority=1)
        self.assertIsNotNone(task_id)
        self.assertIn("task_", task_id)

    def test_get_device_info(self):
        """Test device information retrieval."""
        self.agent.start()
        info = self.agent.get_device_info()
        self.assertEqual(info["device_id"], "test_enhanced_device")
        self.assertEqual(info["device_name"], "Test Phone")
        self.assertEqual(info["os"], "Android")
        self.assertTrue(info["is_active"])

    def test_get_device_stats(self):
        """Test device statistics retrieval."""
        self.agent.start()
        self.agent.send_sms("+1234567890", "msg")
        stats = self.agent.get_device_stats()
        self.assertIn("device", stats)
        self.assertIn("battery", stats)
        self.assertIn("commands_executed", stats)
        self.assertGreater(stats["commands_executed"], 0)

    def test_commands_executed_counter(self):
        """Test that commands executed counter increments correctly."""
        self.agent.start()
        initial = self.agent.commands_executed
        self.agent.send_sms("+1234567890", "msg1")
        self.agent.send_whatsapp("+1234567890", "msg2")
        self.agent.enable_hotspot()
        self.assertEqual(self.agent.commands_executed, initial + 3)


class TestCloudAgent(unittest.TestCase):
    """Test cloud agent functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent = CloudAgent()
    
    def test_start_agent(self):
        """Test agent activation."""
        result = self.agent.start()
        self.assertTrue(result)
        self.assertTrue(self.agent.is_active)
    
    def test_get_uptime(self):
        """Test uptime tracking."""
        self.agent.start()
        uptime = self.agent.get_uptime()
        self.assertIsNotNone(uptime)
        self.assertGreaterEqual(uptime, 0)


if __name__ == "__main__":
    unittest.main()
