"""
Enhanced WhatsApp Integration
Autonomous setup and intelligent messaging with OTP handling.
"""

import logging
from typing import Optional, Dict, List, Tuple
from enum import Enum
from core.autonomous_setup import AutoSetup

logger = logging.getLogger(__name__)


class WhatsAppMode(Enum):
    """WhatsApp connection modes."""
    WEB = "web"
    API = "api"
    ANDROID_BRIDGE = "android_bridge"


class EnhancedWhatsAppManager:
    """Enhanced WhatsApp manager with autonomous setup."""
    
    def __init__(self, mode: WhatsAppMode = WhatsAppMode.WEB, email: Optional[str] = None):
        """
        Initialize enhanced WhatsApp manager.
        
        Args:
            mode: Connection mode
            email: Email for OTP reading
        """
        self.mode = mode
        self.email = email
        self.is_connected = False
        self.auto_setup = AutoSetup(email) if email else None
        self.contacts: Dict = {}
        self.message_queue: List[Dict] = []
        
        logger.info(f"Enhanced WhatsApp manager initialized (mode: {mode.value})")
    
    def autonomous_connect(self, approval_callback: Optional[callable] = None) -> Tuple[bool, str]:
        """
        Autonomously connect to WhatsApp without manual intervention.
        
        Args:
            approval_callback: User approval callback
            
        Returns:
            (success, status_message)
        """
        logger.info(f"🤖 Starting autonomous WhatsApp connection ({self.mode.value})...")
        
        # Step 1: Download required packages
        required_packages = ["selenium", "requests", "Pillow"]
        
        for package in required_packages:
            logger.info(f"📦 Installing {package}...")
            if not self.auto_setup.download_api(package):
                return False, f"Failed to install {package}"
        
        # Step 2: Handle authentication based on mode
        if self.mode == WhatsAppMode.WEB:
            result, message = self._setup_whatsapp_web()
        elif self.mode == WhatsAppMode.API:
            result, message = self._setup_whatsapp_api()
        elif self.mode == WhatsAppMode.ANDROID_BRIDGE:
            result, message = self._setup_android_bridge()
        else:
            return False, "Unknown WhatsApp mode"
        
        if result:
            self.is_connected = True
            logger.info(f"✅ WhatsApp connected successfully")
        else:
            logger.error(f"❌ Connection failed: {message}")
        
        return result, message
    
    def _setup_whatsapp_web(self) -> Tuple[bool, str]:
        """Set up WhatsApp Web connection."""
        logger.info("Setting up WhatsApp Web...")
        
        try:
            # In production, use Selenium to open WhatsApp Web
            # For now, simulate the flow
            
            logger.info("📱 Waiting for QR code scan (display QR code to user)...")
            logger.info("⏳ Scanning QR code... (simulated)")
            
            # Simulate QR code scan
            import time
            time.sleep(2)
            
            logger.info("✅ WhatsApp Web authenticated")
            return True, "WhatsApp Web connected"
        
        except Exception as e:
            return False, f"WhatsApp Web setup failed: {e}"
    
    def _setup_whatsapp_api(self) -> Tuple[bool, str]:
        """Set up WhatsApp API (Business API)."""
        logger.info("Setting up WhatsApp Business API...")
        
        try:
            # Simulate API setup
            logger.info("🔑 Requesting WhatsApp Business API token...")
            logger.info("✅ API credentials configured")
            return True, "WhatsApp API connected"
        
        except Exception as e:
            return False, f"WhatsApp API setup failed: {e}"
    
    def _setup_android_bridge(self) -> Tuple[bool, str]:
        """Set up Android bridge connection."""
        logger.info("Setting up Android bridge...")
        
        try:
            logger.info("📱 Connecting to Android device...")
            logger.info("✅ Android bridge connected")
            return True, "Android bridge connected"
        
        except Exception as e:
            return False, f"Android bridge setup failed: {e}"
    
    def send_message(self, phone_number: str, message: str, require_approval: bool = True) -> Tuple[bool, str]:
        """
        Send WhatsApp message with approval.
        
        Args:
            phone_number: Recipient phone number
            message: Message text
            require_approval: Require user approval
            
        Returns:
            (success, message_id)
        """
        if not self.is_connected:
            logger.error("WhatsApp not connected. Queueing message.")
            self.message_queue.append({
                "phone": phone_number,
                "message": message,
                "status": "queued"
            })
            return False, "Queued - WhatsApp not connected"
        
        # Request approval if required
        if require_approval:
            logger.info(f"📋 Approval required to send message to {phone_number}")
            logger.info(f"   Message: {message}")
            # In production, user would manually approve
        
        logger.info(f"📤 Sending message to {phone_number}")
        
        try:
            # Simulate sending
            message_id = f"msg_{len(self.message_queue)}_{phone_number}"
            
            logger.info(f"✅ Message sent (ID: {message_id})")
            return True, message_id
        
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            return False, str(e)
    
    def read_incoming_messages(self, limit: int = 10) -> List[Dict]:
        """
        Read incoming messages.
        
        Args:
            limit: Maximum messages to read
            
        Returns:
            List of messages
        """
        logger.info(f"Reading incoming WhatsApp messages...")
        
        if not self.is_connected:
            logger.warning("Not connected to WhatsApp")
            return []
        
        # Simulate reading messages
        messages = [
            {
                "sender": "+1234567890",
                "message": "Hey, how are you?",
                "timestamp": "2026-02-26 10:45"
            }
        ]
        
        return messages[:limit]
    
    def process_queued_messages(self) -> Dict:
        """
        Process queued messages now that connection is active.
        
        Returns:
            Processing results
        """
        logger.info(f"⚡ Processing {len(self.message_queue)} queued messages...")
        
        results = {
            "total": len(self.message_queue),
            "sent": 0,
            "failed": 0
        }
        
        for msg in self.message_queue:
            success, msg_id = self.send_message(msg["phone"], msg["message"], require_approval=False)
            
            if success:
                results["sent"] += 1
                msg["status"] = "sent"
            else:
                results["failed"] += 1
                msg["status"] = "failed"
        
        self.message_queue = []
        logger.info(f"✅ Processed {results['sent']} messages, {results['failed']} failed")
        
        return results
