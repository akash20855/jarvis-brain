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
    
    def test_send_sms(self):
        """Test SMS sending."""
        self.agent.start()
        result = self.agent.send_sms("+1234567890", "Test message")
        self.assertTrue(result)


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
