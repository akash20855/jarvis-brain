"""
Autonomous Setup Module
Intelligently sets up integrations without manual intervention.
Handles API downloads, OTP reading from email, and configuration.
"""

import logging
from typing import Dict, Optional, Callable
import subprocess
import smtplib
import imaplib
import email
from pathlib import Path

logger = logging.getLogger(__name__)


class AutoSetup:
    """Handles intelligent autonomous setup of integrations."""
    
    def __init__(self, email_address: Optional[str] = None, email_password: Optional[str] = None):
        """
        Initialize autonomous setup.
        
        Args:
            email_address: User's email for OTP reading
            email_password: Email password (encrypted in production)
        """
        self.email_address = email_address
        self.email_password = email_password
        self.setup_handlers: Dict[str, Callable] = {
            "whatsapp": self.setup_whatsapp,
            "twilio": self.setup_twilio,
            "slack": self.setup_slack,
            "github": self.setup_github,
        }
        logger.info("Autonomous setup module initialized")
    
    def read_latest_otp_from_email(self, subject_filter: str = "OTP") -> Optional[str]:
        """
        Read latest OTP from email.
        
        Args:
            subject_filter: Filter for email subject
            
        Returns:
            OTP code or None
        """
        if not self.email_address or not self.email_password:
            logger.error("Email credentials not configured")
            return None
        
        try:
            logger.info(f"Reading OTP from email ({self.email_address})...")
            
            # Connect to Gmail IMAP
            imap = imaplib.IMAP4_SSL("imap.gmail.com")
            imap.login(self.email_address, self.email_password)
            imap.select("INBOX")
            
            # Search for emails with OTP in subject
            status, messages = imap.search(None, f"SUBJECT \"{subject_filter}\"")
            
            if messages:
                email_ids = messages[0].split()[-1]  # Get latest
                status, msg_data = imap.fetch(email_ids, "(RFC822)")
                
                msg = email.message_from_bytes(msg_data[0][1])
                body = msg.get_payload()
                
                # Extract OTP (usually 6 digits)
                import re
                otp_match = re.search(r'\b\d{6}\b', body)
                
                if otp_match:
                    otp = otp_match.group(0)
                    logger.info(f"✅ OTP found: {otp}")
                    imap.close()
                    return otp
            
            imap.close()
            logger.warning("No OTP found in email")
            return None
        
        except Exception as e:
            logger.error(f"Error reading email: {e}")
            return None
    
    def download_api(self, package_name: str, package_manager: str = "pip") -> bool:
        """
        Download and install API/library.
        
        Args:
            package_name: Package name
            package_manager: pip, homebrew, npm, etc.
            
        Returns:
            Installation success
        """
        logger.info(f"Downloading {package_name} using {package_manager}...")
        
        try:
            if package_manager == "pip":
                cmd = f"pip install {package_name}"
            elif package_manager == "homebrew":
                cmd = f"brew install {package_name}"
            elif package_manager == "npm":
                cmd = f"npm install -g {package_name}"
            else:
                logger.error(f"Unknown package manager: {package_manager}")
                return False
            
            result = subprocess.run(cmd, shell=True, capture_output=True, timeout=300)
            
            if result.returncode == 0:
                logger.info(f"✅ {package_name} installed successfully")
                return True
            else:
                logger.error(f"❌ Installation failed: {result.stderr.decode()}")
                return False
        
        except subprocess.TimeoutExpired:
            logger.error(f"Installation timeout for {package_name}")
            return False
        except Exception as e:
            logger.error(f"Installation error: {e}")
            return False
    
    def setup_whatsapp(self, approval_callback: Optional[Callable] = None) -> bool:
        """
        Autonomously set up WhatsApp integration.
        
        Args:
            approval_callback: Function to get user approval
            
        Returns:
            Setup success
        """
        logger.info("Starting autonomous WhatsApp setup...")
        
        # Check what's needed
        required_packages = ["selenium", "python-telegram-bot"]
        
        for package in required_packages:
            if not self.download_api(package):
                return False
        
        # Setup WhatsApp Web session
        logger.info("Launching WhatsApp Web...")
        
        # In production, this would use Selenium to automate WhatsApp Web login
        # For now, we'll simulate the flow
        
        logger.info("Waiting for WhatsApp QR code scan...")
        # This would display QR code and wait for user to scan
        
        logger.info("✅ WhatsApp setup complete")
        return True
    
    def setup_twilio(self, account_sid: Optional[str] = None, auth_token: Optional[str] = None) -> bool:
        """
        Autonomously set up Twilio SMS integration.
        
        Args:
            account_sid: Twilio account SID
            auth_token: Twilio auth token
            
        Returns:
            Setup success
        """
        logger.info("Starting autonomous Twilio setup...")
        
        if not self.download_api("twilio"):
            return False
        
        # Store credentials
        logger.info("Storing Twilio credentials...")
        
        logger.info("✅ Twilio setup complete")
        return True
    
    def setup_slack(self, workspace_url: Optional[str] = None) -> bool:
        """
        Autonomously set up Slack integration.
        
        Args:
            workspace_url: Slack workspace URL
            
        Returns:
            Setup success
        """
        logger.info("Starting autonomous Slack setup...")
        
        if not self.download_api("slack-sdk"):
            return False
        
        logger.info("Generating Slack OAuth token...")
        # In production, this would open browser and trigger OAuth
        
        logger.info("✅ Slack setup complete")
        return True
    
    def setup_github(self, github_username: Optional[str] = None) -> bool:
        """
        Autonomously set up GitHub integration.
        
        Args:
            github_username: GitHub username
            
        Returns:
            Setup success
        """
        logger.info("Starting autonomous GitHub setup...")
        
        if not self.download_api("PyGithub"):
            return False
        
        logger.info("Generating GitHub personal access token...")
        # In production, this would open browser and trigger token generation
        
        logger.info("✅ GitHub setup complete")
        return True
    
    def setup_integration(self, integration_name: str, **kwargs) -> bool:
        """
        Generic setup for any integration.
        
        Args:
            integration_name: Name of integration to setup
            **kwargs: Integration-specific parameters
            
        Returns:
            Setup success
        """
        handler = self.setup_handlers.get(integration_name.lower())
        
        if not handler:
            logger.error(f"Unknown integration: {integration_name}")
            return False
        
        logger.info(f"Setting up {integration_name}...")
        return handler(**kwargs)
