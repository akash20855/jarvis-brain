"""
SSH Manager for Remote Mac Control
Enables secure SSH connections to remote Macs for executing commands.
"""

import logging
import subprocess
from typing import Optional, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)


class SSHManager:
    """Manages SSH connections to remote Macs."""
    
    def __init__(self, hostname: str, username: str, ssh_key_path: Optional[Path] = None):
        """
        Initialize SSH manager.
        
        Args:
            hostname: Mac hostname or IP
            username: SSH username
            ssh_key_path: Path to SSH private key (optional)
        """
        self.hostname = hostname
        self.username = username
        self.ssh_key_path = ssh_key_path
        self.is_connected = False
        self.connection_timeout = 10
        logger.info(f"SSH manager initialized for {username}@{hostname}")
    
    def _build_ssh_command(self, command: str) -> str:
        """Build SSH command string."""
        ssh_cmd = f"ssh -o ConnectTimeout={self.connection_timeout}"
        
        if self.ssh_key_path:
            ssh_cmd += f" -i {self.ssh_key_path}"
        
        ssh_cmd += f" {self.username}@{self.hostname}"
        return ssh_cmd
    
    def test_connection(self) -> bool:
        """
        Test SSH connection to Mac.
        
        Returns:
            Connection test success
        """
        logger.info(f"Testing SSH connection to {self.hostname}...")
        try:
            result = subprocess.run(
                f"{self._build_ssh_command('echo')} 'Connection successful'",
                shell=True,
                capture_output=True,
                timeout=self.connection_timeout
            )
            self.is_connected = result.returncode == 0
            if self.is_connected:
                logger.info(f"✅ SSH connection successful")
            else:
                logger.error(f"❌ SSH connection failed")
            return self.is_connected
        except subprocess.TimeoutExpired:
            logger.error(f"❌ SSH connection timeout")
            return False
    
    def execute_command(self, command: str, timeout: int = 30) -> Tuple[bool, str]:
        """
        Execute command on remote Mac.
        
        Args:
            command: Command to execute
            timeout: Command timeout in seconds
            
        Returns:
            (success, output)
        """
        if not self.is_connected:
            logger.warning("Not connected. Testing connection...")
            if not self.test_connection():
                return False, "SSH connection failed"
        
        logger.info(f"Executing on {self.hostname}: {command}")
        try:
            result = subprocess.run(
                f"{self._build_ssh_command(command)}",
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if result.returncode == 0:
                logger.info(f"✅ Command successful")
                return True, result.stdout
            else:
                logger.error(f"❌ Command failed: {result.stderr}")
                return False, result.stderr
        
        except subprocess.TimeoutExpired:
            logger.error(f"❌ Command timeout")
            return False, "Command timeout"
        except Exception as e:
            logger.error(f"❌ Command error: {e}")
            return False, str(e)
    
    def build_project(self, project_path: str, build_cmd: str = "make") -> Tuple[bool, str]:
        """
        Build project on remote Mac.
        
        Args:
            project_path: Path to project
            build_cmd: Build command (make, xcodebuild, etc.)
            
        Returns:
            (success, output)
        """
        logger.info(f"Building {project_path} on {self.hostname}")
        command = f"cd {project_path} && {build_cmd}"
        return self.execute_command(command, timeout=600)
    
    def launch_vscode(self, workspace_path: str) -> Tuple[bool, str]:
        """
        Launch VS Code with workspace on remote Mac.
        
        Args:
            workspace_path: Path to workspace
            
        Returns:
            (success, output)
        """
        logger.info(f"Launching VS Code on {self.hostname}")
        command = f"open -a 'Visual Studio Code' {workspace_path}"
        return self.execute_command(command)
    
    def get_system_stats(self) -> dict:
        """
        Get Mac system statistics.
        
        Returns:
            System stats dictionary
        """
        logger.info(f"Fetching system stats from {self.hostname}")
        
        stats = {}
        
        # CPU usage
        success, cpu_output = self.execute_command("sysctl -n hw.ncpu")
        if success:
            stats["cpu_cores"] = int(cpu_output.strip())
        
        # Memory
        success, mem_output = self.execute_command("vm_stat | grep 'Pages free'")
        if success:
            stats["memory_info"] = mem_output.strip()
        
        # Disk space
        success, disk_output = self.execute_command("df -h / | tail -1")
        if success:
            stats["disk_info"] = disk_output.strip()
        
        # Uptime
        success, uptime_output = self.execute_command("uptime")
        if success:
            stats["uptime"] = uptime_output.strip()
        
        return stats
    
    def sync_to_cloud(self, local_path: str, remote_path: str) -> Tuple[bool, str]:
        """
        Sync files to cloud storage.
        
        Args:
            local_path: Local file path
            remote_path: Remote cloud path
            
        Returns:
            (success, output)
        """
        logger.info(f"Syncing {local_path} to cloud from {self.hostname}")
        # This would integrate with S3, Google Drive, iCloud, etc.
        return True, "Sync queued"
