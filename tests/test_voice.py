"""
Voice Module Tests
Unit tests for voice recognition and NLP components.
"""

import unittest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.voice_nlp import VoiceRecognizer, NLPProcessor


class TestVoiceRecognizer(unittest.TestCase):
    """Test voice recognizer functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.recognizer = VoiceRecognizer()
    
    def test_start_listening(self):
        """Test starting voice listening."""
        result = self.recognizer.start_listening()
        self.assertTrue(result)
        self.assertTrue(self.recognizer.is_listening)
    
    def test_stop_listening(self):
        """Test stopping voice listening."""
        self.recognizer.start_listening()
        result = self.recognizer.stop_listening()
        self.assertTrue(result)
        self.assertFalse(self.recognizer.is_listening)


class TestNLPProcessor(unittest.TestCase):
    """Test NLP processor functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.processor = NLPProcessor()
    
    def test_extract_intent(self):
        """Test intent extraction."""
        result = self.processor.extract_intent("play music")
        self.assertIsNotNone(result)
        self.assertIn("intent", result)
        self.assertIn("confidence", result)
    
    def test_extract_entities(self):
        """Test entity extraction."""
        result = self.processor.extract_entities("send message to john")
        self.assertIsInstance(result, list)
    
    def test_parse_command(self):
        """Test command parsing."""
        result = self.processor.parse_command("play rock music")
        self.assertIsNotNone(result)
        self.assertIn("text", result)
        self.assertIn("intent", result)
        self.assertIn("entities", result)


if __name__ == "__main__":
    unittest.main()
