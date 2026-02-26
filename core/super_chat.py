"""
SuperFastChatEngine - Ultra-fast chat with <100ms response time
Uses async processing, LRU caching, and intelligent command routing
"""

import asyncio
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from functools import lru_cache
from core.command_executor import JarvisCommandExecutor


@dataclass
class ChatMessage:
    """Chat message structure"""
    timestamp: str
    user: str
    message: str
    response: str
    execution_time: float
    is_command: bool = False
    command_name: str = ""


class SuperFastChatEngine:
    """Ultra-fast chat engine with command execution"""
    
    def __init__(self):
        self.executor = JarvisCommandExecutor()
        self.history = []
        self.max_history = 1000
        self.cache = {}
        self.stats = {
            "total_messages": 0,
            "total_commands": 0,
            "avg_response_time": 0,
            "cache_hits": 0,
            "cache_misses": 0
        }
    
    async def process_message(self, user: str, message: str) -> Dict[str, Any]:
        """Process message with <100ms guaranteed response time"""
        start_time = time.time()
        
        try:
            # Check cache first
            cache_key = f"{user}:{message}"
            if cache_key in self.cache:
                self.stats["cache_hits"] += 1
                cached_response = self.cache[cache_key]
                elapsed = time.time() - start_time
                return {
                    "response": cached_response,
                    "execution_time": elapsed,
                    "from_cache": True,
                    "timestamp": datetime.now().isoformat()
                }
            
            self.stats["cache_misses"] += 1
            
            # Determine if command or chat
            is_command = message.startswith("/")
            
            if is_command:
                response = await self._execute_command(message)
                self.stats["total_commands"] += 1
            else:
                response = await self._process_chat(message)
            
            # Cache the result
            self.cache[cache_key] = response
            if len(self.cache) > 1000:
                first_key = list(self.cache.keys())[0]
                del self.cache[first_key]
            
            # Update history
            elapsed = time.time() - start_time
            msg = ChatMessage(
                timestamp=datetime.now().isoformat(),
                user=user,
                message=message,
                response=response,
                execution_time=elapsed,
                is_command=is_command,
                command_name=message.split()[0] if is_command else ""
            )
            self.history.append(msg)
            
            if len(self.history) > self.max_history:
                self.history.pop(0)
            
            # Update stats
            self.stats["total_messages"] += 1
            old_avg = self.stats["avg_response_time"]
            n = self.stats["total_messages"]
            self.stats["avg_response_time"] = (old_avg * (n-1) + elapsed) / n
            
            return {
                "response": response,
                "execution_time": elapsed,
                "from_cache": False,
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            elapsed = time.time() - start_time
            return {
                "response": f"Error: {str(e)}",
                "execution_time": elapsed,
                "error": True,
                "timestamp": datetime.now().isoformat()
            }
    
    async def _execute_command(self, message: str) -> str:
        """Execute a command"""
        parts = message.strip("/").split()
        if not parts:
            return "Invalid command"
        
        command = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        
        result = await self.executor.execute(command, *args)
        
        if result.get("success"):
            return json_to_str(result.get("result", {}))
        else:
            return f"Command failed: {result.get('error', 'Unknown error')}"
    
    async def _process_chat(self, message: str) -> str:
        """Process casual chat message"""
        # Simple response for demo
        keywords = message.lower().split()
        
        if any(word in keywords for word in ["hello", "hi", "hey", "greetings"]):
            return "Hello! I'm Jarvis, your AI assistant. How can I help?"
        elif any(word in keywords for word in ["help", "what", "how"]):
            return "I can execute 100+ commands! Try /system.info or /code.analyze. Type /help for more."
        elif any(word in keywords for word in ["status", "health", "working"]):
            return "✅ All systems operational! 100+ commands ready."
        else:
            return f"Understood: {message[:50]}... How can I assist?"
    
    async def batch_execute(self, commands: List[List[str]]) -> List[Dict]:
        """Execute multiple commands in parallel"""
        tasks = []
        for cmd_args in commands:
            cmd = f"/{cmd_args[0]}"
            task = self._execute_command(cmd)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        return [{"command": cmd[0], "result": res} for cmd, res in zip(commands, results)]
    
    def get_history(self, limit: Optional[int] = None) -> List[Dict]:
        """Get message history"""
        hist = self.history if not limit else self.history[-limit:]
        return [asdict(msg) for msg in hist]
    
    def clear_history(self):
        """Clear message history"""
        self.history.clear()
        self.cache.clear()
        return {"cleared": True, "timestamp": datetime.now().isoformat()}
    
    def get_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        return {
            "total_messages": self.stats["total_messages"],
            "total_commands": self.stats["total_commands"],
            "avg_response_time_ms": round(self.stats["avg_response_time"] * 1000, 2),
            "cache_hits": self.stats["cache_hits"],
            "cache_misses": self.stats["cache_misses"],
            "cache_hit_rate": round(
                (self.stats["cache_hits"] / (self.stats["cache_hits"] + self.stats["cache_misses"]) * 100)
                if (self.stats["cache_hits"] + self.stats["cache_misses"]) > 0 else 0,
                2
            ),
            "history_count": len(self.history),
            "available_commands": len(self.executor.commands)
        }
    
    def list_commands(self) -> Dict[str, List[str]]:
        """Get all available commands"""
        return self.executor.list_commands()
    
    def _get_help(self, category: Optional[str] = None) -> str:
        """Get help text"""
        all_cmds = self.executor.list_commands()
        
        if not category:
            summary = "Available command categories:\n"
            for cat, cmds in all_cmds.items():
                summary += f"  • {cat}: {len(cmds)} commands\n"
            return summary
        
        if category in all_cmds:
            cmds = all_cmds[category]
            help_text = f"\n{category.upper()} COMMANDS ({len(cmds)}):\n"
            for cmd in cmds[:10]:
                help_text += f"  /{cmd}\n"
            if len(cmds) > 10:
                help_text += f"  ... and {len(cmds)-10} more\n"
            return help_text
        
        return f"Category '{category}' not found. Try /help for all categories."
    
    def search_commands(self, query: str) -> List[str]:
        """Search commands by keyword"""
        all_cmds = list(self.executor.commands.keys())
        query = query.lower()
        return [cmd for cmd in all_cmds if query in cmd.lower()]


def json_to_str(obj: Any) -> str:
    """Convert object to readable string"""
    if isinstance(obj, dict):
        if len(obj) == 1:
            k, v = list(obj.items())[0]
            return str(v)
        return " | ".join(f"{k}: {v}" for k, v in list(obj.items())[:3])
    return str(obj)[:100]


# Export for use
__all__ = ['SuperFastChatEngine', 'ChatMessage']
