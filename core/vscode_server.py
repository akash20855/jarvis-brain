"""
Enhanced VS Code Integration with WebSocket API
Enables real-time communication between VS Code and JARVIS
"""

import json
import logging
import os
import sys
import threading
from datetime import datetime
from pathlib import Path
from typing import Callable, Dict

# Load environment variables first
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("VSCodeIntegration")

# Add workspace to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from websocket_server import WebsocketServer

# Import with fallbacks
try:
    from core.simple_chatbot import SimpleChatbot
except ImportError as e:
    logger.warning(f"SimpleChatbot not available: {e}")
    SimpleChatbot = None

try:
    from core.simple_calculator import Calculator
except ImportError as e:
    logger.warning(f"Calculator not available: {e}")
    Calculator = None

try:
    from core.claude_code_generator import ClaudeCodeGenerator
except ImportError as e:
    logger.error(f"Failed to import ClaudeCodeGenerator: {e}")
    ClaudeCodeGenerator = None

try:
    from core.ollama_code_generator import OllamaCodeGenerator
except ImportError as e:
    logger.warning(f"OllamaCodeGenerator not available: {e}")
    OllamaCodeGenerator = None

try:
    from core.groq_code_generator import GroqCodeGenerator
except ImportError as e:
    logger.warning(f"GroqCodeGenerator not available: {e}")
    GroqCodeGenerator = None

try:
    from core.auto_debug import AutoDebugEngine
except ImportError as e:
    logger.warning(f"AutoDebugEngine not available: {e}")
    AutoDebugEngine = None

try:
    from core.autonomous_self_improvement import AutonomousSelfImprovementEngine
except ImportError as e:
    logger.warning(f"AutonomousSelfImprovementEngine not available: {e}")
    AutonomousSelfImprovementEngine = None

AI_BACKEND = os.getenv('AI_BACKEND', 'claude').lower()  # 'claude' or 'ollama'


class VSCodeCommand:
    """Represents a command that can be executed through VS Code"""
    
    def __init__(self, name: str, description: str, handler: Callable):
        self.name = name
        self.description = description
        self.handler = handler
        self.last_execution = None
        self.execution_count = 0
    
    def execute(self, *args, **kwargs):
        """Execute the command"""
        self.last_execution = datetime.now()
        self.execution_count += 1
        return self.handler(*args, **kwargs)


class VSCodeIntegrationServer:
    """WebSocket server for VS Code integration"""
    
    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.server = WebsocketServer(host=host, port=port)
        self.clients = []
        self.commands: Dict[str, VSCodeCommand] = {}
        self.setup_handlers()
        self.setup_commands()
        
        # Initialize simple chatbot for quick responses
        try:
            self.simple_bot = SimpleChatbot() if SimpleChatbot else None
            if self.simple_bot:
                logger.info("✓ SimpleChatbot initialized for fallback responses")
        except Exception as e:
            logger.warning(f"Failed to initialize SimpleChatbot: {e}")
            self.simple_bot = None
        
        # Initialize simple calculator
        try:
            self.calculator = Calculator() if Calculator else None
            if self.calculator:
                logger.info("✓ Calculator initialized for math operations")
        except Exception as e:
            logger.warning(f"Failed to initialize Calculator: {e}")
            self.calculator = None
        
        # Initialize JARVIS components with fallbacks
        self.ai_backend = AI_BACKEND
        
        if AI_BACKEND == 'groq':
            try:
                self.claude = GroqCodeGenerator() if GroqCodeGenerator else None
                logger.info("✓ Using Groq AI backend (free & fast)")
            except Exception as e:
                logger.error(f"❌ Groq initialization failed: {e}")
                logger.error("🔧 FIX: Set your GROQ_API_KEY in .env:")
                logger.error("   GROQ_API_KEY=gsk-xxxxx")
                logger.error("   Get free key: https://console.groq.com/keys")
                self.claude = None
        elif AI_BACKEND == 'ollama':
            try:
                self.claude = OllamaCodeGenerator() if OllamaCodeGenerator else None
                logger.info("✓ Using Ollama AI backend (local, free)")
            except Exception as e:
                logger.warning(f"Failed to initialize Ollama, falling back to Claude: {e}")
                self.claude = ClaudeCodeGenerator() if ClaudeCodeGenerator else None
                self.ai_backend = 'claude'
        else:
            try:
                self.claude = ClaudeCodeGenerator() if ClaudeCodeGenerator else None
                logger.info("✓ Using Claude AI backend")
            except ValueError as e:
                # API key issue
                logger.error(f"❌ Claude initialization failed: {e}")
                logger.error("🔧 FIX: Set your ANTHROPIC_API_KEY in .env:")
                logger.error("   ANTHROPIC_API_KEY=sk-ant-xxxxx")
                logger.error("   Get free key: https://console.anthropic.com/account/keys")
                self.claude = None
            except Exception as e:
                logger.warning(f"Failed to initialize Claude: {e}")
                self.claude = None
        
        try:
            self.debugger = AutoDebugEngine() if AutoDebugEngine else None
        except Exception as e:
            logger.warning(f"Failed to initialize Debugger: {e}")
            self.debugger = None
        
        try:
            self.improver = AutonomousSelfImprovementEngine() if AutonomousSelfImprovementEngine else None
        except Exception as e:
            logger.warning(f"Failed to initialize Improver: {e}")
            self.improver = None
        
        self.server.set_fn_new_client(self.on_new_client)
        self.server.set_fn_client_left(self.on_client_left)
        self.server.set_fn_message_received(self.on_message_received)
        
        logger.info(f"VS Code Integration Server initialized on ws://{host}:{port}")
    
    def setup_handlers(self):
        """Setup WebSocket event handlers"""
        pass
    
    def setup_commands(self):
        """Setup all available commands for VS Code"""
        
        self.register_command(
            "jarvis.generateCode",
            "Generate code using Claude",
            self.cmd_generate_code
        )
        
        self.register_command(
            "jarvis.analyzeCode",
            "Analyze code for improvements",
            self.cmd_analyze_code
        )
        
        self.register_command(
            "jarvis.debugProject",
            "Debug current project",
            self.cmd_debug_project
        )
        
        self.register_command(
            "jarvis.improveCode",
            "Auto-improve code",
            self.cmd_improve_code
        )
        
        self.register_command(
            "jarvis.generateTests",
            "Generate unit tests",
            self.cmd_generate_tests
        )
        
        self.register_command(
            "jarvis.refactorCode",
            "Refactor selected code",
            self.cmd_refactor_code
        )
        
        self.register_command(
            "jarvis.explainCode",
            "Explain code in detail",
            self.cmd_explain_code
        )
        
        self.register_command(
            "jarvis.buildProject",
            "Build project with debugging",
            self.cmd_build_project
        )
        
        self.register_command(
            "jarvis.status",
            "Get JARVIS status",
            self.cmd_status
        )
        
        self.register_command(
            "jarvis.chat",
            "Chat with JARVIS AI",
            self.cmd_chat
        )
    
    def register_command(self, name: str, description: str, handler: Callable):
        """Register a command"""
        self.commands[name] = VSCodeCommand(name, description, handler)
        logger.info(f"Registered command: {name}")
    
    def on_new_client(self, client, server):
        """Handle new client connection"""
        self.clients.append(client)
        logger.info(f"New VS Code client connected from {client['address']}")
        
        # Send welcome message with all commands
        welcome = {
            "type": "welcome",
            "message": "Connected to JARVIS",
            "commands": list(self.commands.keys()),
            "timestamp": datetime.now().isoformat()
        }
        server.send_message(client, json.dumps(welcome))
    
    def on_client_left(self, client, server):
        """Handle client disconnection"""
        if client in self.clients:
            self.clients.remove(client)
        logger.info(f"VS Code client disconnected from {client['address']}")
    
    def on_message_received(self, client, server, message):
        """Handle incoming message from VS Code"""
        try:
            data = json.loads(message)
            command = data.get("command")
            args = data.get("args", [])
            kwargs = data.get("kwargs", {})
            
            if command in self.commands:
                logger.info(f"Executing command: {command}")
                result = self.commands[command].execute(*args, **kwargs)
                
                response = {
                    "type": "response",
                    "command": command,
                    "result": result,
                    "success": True,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                response = {
                    "type": "error",
                    "command": command,
                    "error": f"Unknown command: {command}",
                    "available_commands": list(self.commands.keys()),
                    "success": False
                }
            
            server.send_message(client, json.dumps(response))
        except json.JSONDecodeError:
            response = {
                "type": "error",
                "error": "Invalid JSON",
                "success": False
            }
            server.send_message(client, json.dumps(response))
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            response = {
                "type": "error",
                "error": str(e),
                "success": False
            }
            server.send_message(client, json.dumps(response))
    
    def broadcast(self, message: Dict):
        """Send message to all connected clients"""
        msg_str = json.dumps(message)
        for client in self.clients:
            self.server.send_message(client, msg_str)
    
    # Command implementations
    def cmd_generate_code(self, description: str, language: str = "python"):
        """Generate code"""
        try:
            if not self.claude:
                raise Exception("Claude code generator not available")
            result = self.claude.generate_code(description, language)
            return {
                "code": result,
                "language": language
            }
        except Exception as e:
            raise Exception(f"Code generation failed: {e}")
    
    def cmd_analyze_code(self, code: str, language: str = "python"):
        """Analyze code"""
        try:
            if not self.claude:
                raise Exception("Claude code analyzer not available")
            result = self.claude.analyze_code(code, language)
            return {
                "analysis": result,
                "language": language
            }
        except Exception as e:
            raise Exception(f"Code analysis failed: {e}")
    
    def cmd_debug_project(self, file_path: str = None):
        """Debug project or specific file"""
        try:
            if not self.debugger:
                raise Exception("Debug engine not available")
            if file_path:
                issues = self.debugger.analyze_file(file_path)
            else:
                issues = self.debugger.scan_directory(".", max_files=10)
            
            return {
                "issues_found": len(issues),
                "issues": issues[:5],  # Return first 5
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            raise Exception(f"Debug failed: {e}")
    
    def cmd_improve_code(self, file_count: int = 5):
        """Auto-improve code"""
        try:
            if not self.improver:
                raise Exception("Improver not available")
            improved = self.improver.improve_project(max_files=file_count)
            return {
                "files_improved": improved,
                "count": len(improved),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            raise Exception(f"Code improvement failed: {e}")
    
    def cmd_generate_tests(self, code: str, language: str = "python"):
        """Generate unit tests"""
        try:
            if not self.claude:
                return {
                    "success": False,
                    "error": "Claude AI backend not available",
                    "help": "Set ANTHROPIC_API_KEY in .env file. Get free key: https://console.anthropic.com/account/keys",
                    "status": "needs_api_key"
                }

            result = self.claude.generate_test(code, language)
            return {
                "success": True,
                "tests": result,
                "language": language
            }
        except Exception as e:
            logger.error(f"Test generation error: {e}")
            return {
                "success": False,
                "error": f"Test generation failed: {e}",
                "language": language
            }
    
    def cmd_refactor_code(self, code: str, language: str = "python"):
        """Refactor code"""
        try:
            if not self.claude:
                raise Exception("Claude not available")
            result = self.claude.refactor_code(code, language)
            return {
                "refactored": result,
                "language": language
            }
        except Exception as e:
            raise Exception(f"Refactoring failed: {e}")
    
    def cmd_explain_code(self, code: str, language: str = "python"):
        """Explain code"""
        try:
            if not self.claude:
                raise Exception("Claude not available")
            result = self.claude.explain_code(code, language)
            return {
                "explanation": result,
                "language": language
            }
        except Exception as e:
            raise Exception(f"Code explanation failed: {e}")
    
    def cmd_build_project(self):
        """Build project with debugging"""
        try:
            from core.advanced_build import AdvancedBuildSystem
            builder = AdvancedBuildSystem()
            builder.execute_build()
            
            return {
                "status": "success",
                "total_time": sum(p.duration for p in builder.phases),
                "phases_completed": len(builder.phases),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            raise Exception(f"Build failed: {e}")
    
    def cmd_status(self):
        """Get JARVIS status"""
        return {
            "status": "online",
            "version": "2.0.0",
            "components": {
                "claude": "online",
                "debugger": "online",
                "improver": "online"
            },
            "connected_clients": len(self.clients),
            "available_commands": len(self.commands),
            "timestamp": datetime.now().isoformat()
        }
    
    def cmd_chat(self, message: str):
        """Chat with JARVIS"""
        try:
            lower_msg = message.lower().strip()
            
            # Check for calculator operations
            if self.calculator:
                # Handle various math expressions
                if any(op in lower_msg for op in [' + ', ' - ', ' * ', ' / ', ' ^ ', '√', 'plus', 'minus', 'times', 'divided', 'add', 'subtract', 'multiply', 'divide', 'power', 'sqrt']):
                    # Try to parse and calculate simple math expressions
                    # Format: "5 + 3", "10 * 2", "100 / 4", etc.
                    for op_symbol, op_name in [('+', 'add'), ('-', 'subtract'), ('*', 'multiply'), ('/', 'divide'), ('^', 'power'), ('**', 'power')]:
                        if op_symbol in message:
                            try:
                                parts = message.split(op_symbol)
                                if len(parts) == 2:
                                    num1 = float(parts[0].strip())
                                    num2 = float(parts[1].strip())
                                    result = self.calculator.calculate(op_name, num1, num2)
                                    
                                    # Validate result is a number
                                    if isinstance(result, (int, float)):
                                        return {
                                            "success": True,
                                            "response": f"{message} = {result}",
                                            "backend": "calculator",
                                            "timestamp": datetime.now().isoformat()
                                        }
                                    else:
                                        # Result is an error message string
                                        return {
                                            "success": True,
                                            "response": result,
                                            "backend": "calculator",
                                            "timestamp": datetime.now().isoformat()
                                        }
                            except ZeroDivisionError:
                                return {
                                    "success": True,
                                    "response": "Cannot divide by zero. Please try another calculation.",
                                    "backend": "calculator",
                                    "timestamp": datetime.now().isoformat()
                                }
                            except (ValueError, TypeError):
                                continue
                            except Exception as calc_error:
                                logger.debug(f"Calculation error: {calc_error}")
                                continue
            
            # Try simple chatbot for quick responses
            if self.simple_bot:
                simple_response = self.simple_bot.respond(message)
                if simple_response:
                    return {
                        "success": True,
                        "response": simple_response,
                        "backend": "simple_chatbot",
                        "timestamp": datetime.now().isoformat()
                    }
            
            # Fall back to AI backend for more complex responses
            if not self.claude:
                return {
                    "success": False,
                    "error": "No AI backend available",
                    "message": "Please configure an AI backend (Groq, Claude, or Ollama)"
                }
            
            # Use the AI backend to respond conversationally
            response = self.claude.generate_code(f"Respond conversationally to: {message}")
            
            # Extract just the text/code from the response dict
            response_text = response.get("code", "") if isinstance(response, dict) else str(response)
            
            return {
                "success": True,
                "response": response_text,
                "backend": self.ai_backend,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Chat failed: {e}"
            }
    
    def start(self):
        """Start the server"""
        logger.info(f"Starting VS Code Integration Server on ws://{self.host}:{self.port}")
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            logger.info("Server stopped")
    
    def start_async(self):
        """Start server in background thread"""
        thread = threading.Thread(target=self.start, daemon=True)
        thread.start()
        logger.info("VS Code Integration Server started in background")
        return thread


def create_vscode_integration():
    """Create and start VS Code integration server"""
    try:
        server = VSCodeIntegrationServer(host="localhost", port=8765)
        return server
    except ImportError:
        logger.warning("websocket-server not installed. Installing...")
        import subprocess
        subprocess.run(["pip", "install", "websocket-server"], check=True)
        return VSCodeIntegrationServer(host="localhost", port=8765)


if __name__ == "__main__":
    server = create_vscode_integration()
    server.start()
