"""
Continuous Listening Service
Always-on microphone with wake word detection for 24/7 listening.
"""

import logging
import threading
from typing import Optional, Callable
from datetime import datetime

logger = logging.getLogger(__name__)


class WakeWordDetector:
    """Detects wake word to trigger Jarvis."""
    
    def __init__(self, wake_word: str = "jarvis", sensitivity: float = 0.5):
        """
        Initialize wake word detector.
        
        Args:
            wake_word: Wake word to listen for
            sensitivity: Detection sensitivity (0-1)
        """
        self.wake_word = wake_word.lower()
        self.sensitivity = sensitivity
        self.is_listening = False
        logger.info(f"Wake word detector initialized (word: '{wake_word}')")
    
    def detect(self, audio_text: str) -> bool:
        """
        Detect wake word in audio text.
        
        Args:
            audio_text: Transcribed audio text
            
        Returns:
            Wake word detected
        """
        if self.wake_word in audio_text.lower():
            logger.info(f"🔔 Wake word detected: '{audio_text}'")
            return True
        return False


class ContinuousListeningService:
    """Always-on microphone service for 24/7 voice command listening."""
    
    def __init__(self, device_type: str = "mac", on_wake_word_callback: Optional[Callable] = None):
        """
        Initialize listening service.
        
        Args:
            device_type: Device type (mac, android, cloud)
            on_wake_word_callback: Callback when wake word detected
        """
        self.device_type = device_type
        self.on_wake_word_callback = on_wake_word_callback
        self.is_listening = False
        self.listening_start_time = None
        self.wake_word_detector = WakeWordDetector()
        self.commands_heard = 0
        self.listening_thread = None
        logger.info(f"Continuous listening service initialized ({device_type})")
    
    def start_listening(self) -> bool:
        """Start listening for wake word."""
        logger.info(f"🎤 Starting continuous listening on {self.device_type}...")
        self.is_listening = True
        self.listening_start_time = datetime.now()
        
        # Start listening in background thread
        self.listening_thread = threading.Thread(target=self._listening_loop, daemon=True)
        self.listening_thread.start()
        
        return True
    
    def stop_listening(self) -> bool:
        """Stop listening."""
        logger.info("🛑 Stopping listening service...")
        self.is_listening = False
        return True
    
    def _listening_loop(self):
        """Background listening loop."""
        while self.is_listening:
            # Simulate listening (in production, use SpeechRecognition or audio stream)
            # This would continuously capture and transcribe audio
            pass
    
    def get_listening_duration(self) -> float:
        """
        Get listening duration in seconds.
        
        Returns:
            Duration in seconds
        """
        if not self.listening_start_time:
            return 0
        return (datetime.now() - self.listening_start_time).total_seconds()
    
    def get_listening_stats(self) -> dict:
        """
        Get listening statistics.
        
        Returns:
            Stats dictionary
        """
        return {
            "is_listening": self.is_listening,
            "device": self.device_type,
            "duration_seconds": self.get_listening_duration(),
            "commands_heard": self.commands_heard,
            "start_time": self.listening_start_time.isoformat() if self.listening_start_time else None
        }
    
    def process_audio_stream(self, audio_text: str) -> bool:
        """
        Process audio stream and detect wake word.
        
        Args:
            audio_text: Transcribed audio
            
        Returns:
            Wake word detected
        """
        if self.wake_word_detector.detect(audio_text):
            self.commands_heard += 1
            logger.info(f"✅ Command #{self.commands_heard} detected")
            
            # Trigger callback
            if self.on_wake_word_callback:
                self.on_wake_word_callback(audio_text)
            
            return True
        
        return False


class MultiDeviceListeningManager:
    """Manages listening across multiple devices (Mac, Android, Cloud)."""
    
    def __init__(self):
        """Initialize multi-device listening manager."""
        self.listeners: dict = {
            "mac": ContinuousListeningService(device_type="mac"),
            "android": ContinuousListeningService(device_type="android"),
            "cloud": ContinuousListeningService(device_type="cloud"),
        }
        self.active_device = None
        logger.info("Multi-device listening manager initialized")
    
    def start_on_device(self, device_type: str) -> bool:
        """
        Start listening on specific device.
        
        Args:
            device_type: Device type (mac, android, cloud)
            
        Returns:
            Success status
        """
        if device_type not in self.listeners:
            logger.error(f"Unknown device type: {device_type}")
            return False
        
        # Stop listening on other devices
        for name, listener in self.listeners.items():
            if name != device_type:
                listener.stop_listening()
        
        # Start listening on target device
        self.active_device = device_type
        logger.info(f"🎤 Switching listening to {device_type}...")
        return self.listeners[device_type].start_listening()
    
    def switch_device(self, from_device: str, to_device: str) -> bool:
        """
        Switch listening from one device to another.
        
        Args:
            from_device: Source device
            to_device: Target device
            
        Returns:
            Success status
        """
        logger.info(f"🔄 Switching listening: {from_device} → {to_device}")
        
        if from_device in self.listeners:
            self.listeners[from_device].stop_listening()
        
        return self.start_on_device(to_device)
    
    def get_all_stats(self) -> dict:
        """
        Get listening stats from all devices.
        
        Returns:
            Stats from all devices
        """
        return {
            device: listener.get_listening_stats()
            for device, listener in self.listeners.items()
        }
    
    def get_active_listener(self) -> Optional[ContinuousListeningService]:
        """Get currently active listener."""
        if self.active_device:
            return self.listeners.get(self.active_device)
        return None
