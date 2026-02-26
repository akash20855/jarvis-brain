"""
Enhanced Mac Agent with SSH Control and Advanced Capabilities
Extended functionality for comprehensive Mac control.
"""

import logging
import subprocess
from typing import Optional, Dict, List, Tuple
from core.ssh_manager import SSHManager

logger = logging.getLogger(__name__)


class EnhancedMacAgent:
    """Enhanced Mac agent with SSH and advanced capabilities."""
    
    def __init__(self, hostname: str, username: str, use_ssh: bool = False, ssh_key_path: Optional[str] = None):
        """
        Initialize enhanced Mac agent.
        
        Args:
            hostname: Mac hostname or IP
            username: SSH username (if using SSH)
            use_ssh: Whether to use SSH for remote control
            ssh_key_path: Path to SSH key (if using SSH)
        """
        self.hostname = hostname
        self.username = username
        self.is_active = False
        self.use_ssh = use_ssh
        self.ssh_manager = None
        
        if use_ssh:
            from pathlib import Path
            key_path = Path(ssh_key_path) if ssh_key_path else None
            self.ssh_manager = SSHManager(hostname, username, key_path)
        
        logger.info(f"Enhanced Mac agent initialized for {hostname}")
    
    def start(self) -> bool:
        """Start Mac agent."""
        self.is_active = True
        logger.info("Mac agent started")
        
        if self.use_ssh and self.ssh_manager:
            return self.ssh_manager.test_connection()
        return True
    
    def stop(self) -> bool:
        """Stop Mac agent."""
        self.is_active = False
        logger.info("Mac agent stopped")
        return True
    
    def _execute(self, command: str, timeout: int = 30) -> Tuple[bool, str]:
        """
        Execute command locally or via SSH.
        
        Args:
            command: Command to execute
            timeout: Command timeout
            
        Returns:
            (success, output)
        """
        if self.use_ssh and self.ssh_manager:
            return self.ssh_manager.execute_command(command, timeout)
        else:
            try:
                result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout)
                return result.returncode == 0, result.stdout or result.stderr
            except subprocess.TimeoutExpired:
                return False, "Command timeout"
            except Exception as e:
                return False, str(e)
    
    def build_project(self, project_path: str, build_type: str = "debug") -> bool:
        """
        Build project.
        
        Args:
            project_path: Path to project
            build_type: Build type (debug/release)
            
        Returns:
            Build success
        """
        logger.info(f"Building project: {project_path} ({build_type})")
        
        # Detect build system
        build_cmd = self._detect_build_system(project_path)
        if not build_cmd:
            logger.error("Could not detect build system")
            return False
        
        success, output = self._execute(f"cd {project_path} && {build_cmd}")
        logger.info(f"Build {'completed' if success else 'failed'}: {output[:100]}")
        return success
    
    def _detect_build_system(self, project_path: str) -> Optional[str]:
        """Detect project build system."""
        # Check for common build files
        checks = [
            (f"{project_path}/Makefile", "make"),
            (f"{project_path}/CMakeLists.txt", "cmake . && make"),
            (f"{project_path}/build.gradle", "gradle build"),
            (f"{project_path}/package.json", "npm run build"),
            (f"{project_path}/setup.py", "python setup.py build"),
            (f"{project_path}/*.xcodeproj", "xcodebuild"),
        ]
        
        for file_path, build_cmd in checks:
            success, _ = self._execute(f"test -f {file_path} && echo exists")
            if success:
                return build_cmd
        
        return None
    
    def run_tests(self, test_path: str) -> Tuple[bool, str]:
        """
        Run tests.
        
        Args:
            test_path: Path to tests
            
        Returns:
            (success, output)
        """
        logger.info(f"Running tests: {test_path}")
        return self._execute(f"cd {test_path} && pytest -v", timeout=300)
    
    def deploy_to_cloud(self, source_path: str, destination: str) -> bool:
        """
        Deploy to cloud storage.
        
        Args:
            source_path: Local source path
            destination: Cloud destination
            
        Returns:
            Deployment success
        """
        logger.info(f"Deploying {source_path} to {destination}")
        
        # Example: S3 deployment
        if "s3://" in destination:
            cmd = f"aws s3 sync {source_path} {destination}"
        # Example: GitHub deployment
        elif "github.com" in destination:
            cmd = f"git push origin main"
        else:
            return False
        
        success, output = self._execute(cmd, timeout=600)
        return success
    
    def get_system_info(self) -> Dict:
        """Get detailed Mac system information."""
        logger.info("Fetching system information")
        
        if self.use_ssh and self.ssh_manager:
            return self.ssh_manager.get_system_stats()
        
        info = {}
        
        # Get CPU info
        success, output = self._execute("sysctl -n hw.ncpu")
        info["cpu_cores"] = int(output.strip()) if success else None
        
        # Get memory info
        success, output = self._execute("vm_stat | grep 'Pages free'")
        info["memory"] = output.strip() if success else None
        
        # Get OS version
        success, output = self._execute("sw_vers -productVersion")
        info["os_version"] = output.strip() if success else None
        
        return info
    
    def monitor_performance(self) -> Dict:
        """
        Monitor Mac performance.
        
        Returns:
            Performance metrics
        """
        logger.info("Monitoring performance")
        
        metrics = {}
        
        # CPU usage
        success, output = self._execute("top -l 1 -n 1 | grep 'CPU usage'")
        metrics["cpu_usage"] = output.strip() if success else "unknown"
        
        # Memory usage
        success, output = self._execute("vm_stat | grep 'Pages active'")
        metrics["memory_active"] = output.strip() if success else "unknown"
        
        # Disk usage
        success, output = self._execute("df -h / | tail -1")
        metrics["disk_usage"] = output.strip() if success else "unknown"
        
        return metrics
    
    def sync_to_cloud(self, local_path: str, cloud_path: str = "s3://jarvis-backups") -> bool:
        """
        Sync files to cloud.
        
        Args:
            local_path: Local path to sync
            cloud_path: Cloud destination path
            
        Returns:
            Sync success
        """
        logger.info(f"Syncing {local_path} to cloud")
        
        cmd = f"aws s3 sync {local_path} {cloud_path}"
        success, output = self._execute(cmd, timeout=600)
        
        if success:
            logger.info(f"✅ Sync successful")
        else:
            logger.error(f"❌ Sync failed: {output}")
        
        return success
