"""
Security Module Tests
Unit tests for authentication, logging, and rollback.
"""

import unittest
import sys
from pathlib import Path
import tempfile

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.security import AuthenticationManager, AuditLogger, RollbackManager


class TestAuthenticationManager(unittest.TestCase):
    """Test authentication manager."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.auth_manager = AuthenticationManager()
    
    def test_authenticate(self):
        """Test authentication."""
        result = self.auth_manager.authenticate("user", "password")
        self.assertFalse(result)  # Should fail with placeholder implementation


class TestAuditLogger(unittest.TestCase):
    """Test audit logger."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.logger = AuditLogger(Path(self.temp_dir.name))
    
    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()
    
    def test_log_event(self):
        """Test event logging."""
        self.logger.log_event("test_event", {"detail": "test"})
        # Event should be logged
    
    def test_log_failed_access(self):
        """Test failed access logging."""
        self.logger.log_failed_access("user", "invalid_password")


class TestRollbackManager(unittest.TestCase):
    """Test rollback manager."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.manager = RollbackManager(Path(self.temp_dir.name))
    
    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()
    
    def test_create_snapshot(self):
        """Test snapshot creation."""
        result = self.manager.create_snapshot("test_snapshot")
        self.assertTrue(result)
        self.assertIn("test_snapshot", self.manager.snapshots)
    
    def test_rollback_to_snapshot(self):
        """Test rollback to snapshot."""
        self.manager.create_snapshot("test_snapshot")
        result = self.manager.rollback_to("test_snapshot")
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
