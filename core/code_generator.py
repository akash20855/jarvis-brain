"""
Code Generator - Creates and executes code based on AI requests
"""

import os
import json
import subprocess
import requests
import shutil
from datetime import datetime
from pathlib import Path

class CodeGenerator:
    """Generate and execute code from natural language requests"""
    
    def __init__(self, workspace_dir=None, ai_url="http://host.docker.internal:11434"):
        self.workspace_dir = workspace_dir or Path(__file__).parent.parent / "generated_code"
        self.ai_url = ai_url
        self.created_files = []
        
        # Create workspace if not exists
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_code(self, request: str, language: str = "python") -> dict:
        """Generate code from natural language request using AI"""
        try:
            # Prompt for AI to generate code
            prompt = f"""User requested: "{request}"

Generate complete, working {language} code that fulfills this request.
Include error handling and comments.
Make the code production-ready.

Return ONLY the code in a code block, no explanations before or after:

```{language}
[YOUR CODE HERE]
```"""
            
            response = requests.post(
                f"{self.ai_url}/api/generate",
                json={
                    "model": "mistral",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                code = response.json().get("response", "").strip()
                
                # Extract code from markdown code blocks if present
                if "```" in code:
                    # Find code blocks
                    parts = code.split("```")
                    # Get the content between the first and second backticks
                    if len(parts) >= 2:
                        code_block = parts[1]
                        # Remove language identifier if present (e.g., ```python -> python)
                        lines = code_block.split("\n")
                        if lines[0].strip().lower() in ["python", "javascript", "html", "bash", "java", "cpp", "csharp"]:
                            code = "\n".join(lines[1:])
                        else:
                            code = code_block
                        code = code.strip()
                
                # Remove any remaining explanatory text
                # If code doesn't start with expected patterns, find the first line that looks like code
                if code and not any(code.startswith(p) for p in ["def ", "class ", "import ", "function ", "<", "#!/", "echo"]):
                    lines = code.split("\n")
                    code_start = 0
                    for i, line in enumerate(lines):
                        if any(line.strip().startswith(p) for p in ["def ", "class ", "import ", "function ", "<", "#!/", "echo", "var ", "const ", "let "]):
                            code_start = i
                            break
                    if code_start > 0:
                        code = "\n".join(lines[code_start:])
                
                return {
                    "success": True,
                    "code": code,
                    "language": language
                }
            else:
                return {
                    "success": False,
                    "error": f"AI service returned {response.status_code}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def save_code(self, code: str, filename: str, language: str = "python") -> dict:
        """Save generated code to file"""
        try:
            # Determine file extension
            ext_map = {
                "python": ".py",
                "javascript": ".js",
                "html": ".html",
                "bash": ".sh"
            }
            ext = ext_map.get(language, ".txt")
            
            # Create file path
            file_path = self.workspace_dir / f"{filename}{ext}"
            
            # Write code to file
            file_path.write_text(code)
            
            self.created_files.append({
                "filename": filename + ext,
                "path": str(file_path),
                "language": language,
                "created_at": datetime.now().isoformat()
            })
            
            return {
                "success": True,
                "filepath": str(file_path),
                "filename": filename + ext,
                "message": f"Code saved to {filename}{ext}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def execute_code(self, filepath: str) -> dict:
        """Execute generated code"""
        try:
            file_path = Path(filepath)
            
            if not file_path.exists():
                return {"success": False, "error": "File not found"}
            
            # Determine how to execute based on file type
            if filepath.endswith(".py"):
                result = subprocess.run(
                    ["python3", filepath],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
            elif filepath.endswith(".sh"):
                result = subprocess.run(
                    ["bash", filepath],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
            else:
                return {"success": False, "error": "Unsupported file type"}
            
            return {
                "success": True,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Code execution timed out"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def open_in_vscode(self, filepath: str) -> dict:
        """Open generated file in VS Code"""
        try:
            # Method 1: Try 'code' command (if in PATH)
            code_cmd = shutil.which("code")
            
            if code_cmd:
                subprocess.Popen([code_cmd, filepath])
            else:
                # Method 2: Use full path to VS Code on macOS
                vs_code_path = "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"
                if os.path.exists(vs_code_path):
                    subprocess.Popen([vs_code_path, filepath])
                else:
                    # Method 3: Use 'open' command (macOS) to open with default editor
                    subprocess.Popen(["open", "-a", "Visual Studio Code", filepath])
            
            return {
                "success": True,
                "message": f"Opening {filepath} in VS Code",
                "filepath": filepath
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"⚠️ Could not auto-open in VS Code: {str(e)} - File saved at {filepath}"
            }
    
    def create_and_open(self, request: str, filename: str = None, language: str = "python") -> dict:
        """Generate code, save it, and open in VS Code"""
        # Generate code
        gen_result = self.generate_code(request, language)
        if not gen_result["success"]:
            return gen_result
        
        code = gen_result["code"]
        
        # Use filename from request if not provided
        if not filename:
            filename = request.split()[0].lower()
            if language == "python":
                filename = filename.replace(" ", "_")
        
        # Save code
        save_result = self.save_code(code, filename, language)
        if not save_result["success"]:
            return save_result
        
        filepath = save_result["filepath"]
        
        # Open in VS Code
        vscode_result = self.open_in_vscode(filepath)
        if not vscode_result["success"]:
            return vscode_result
        
        return {
            "success": True,
            "code": code,
            "filepath": filepath,
            "filename": save_result["filename"],
            "message": f"Created and opened {save_result['filename']} in VS Code",
            "vscode_opened": True
        }
    
    def list_generated(self) -> dict:
        """List all generated files"""
        return {
            "success": True,
            "workspace": str(self.workspace_dir),
            "files": self.created_files,
            "total": len(self.created_files)
        }
