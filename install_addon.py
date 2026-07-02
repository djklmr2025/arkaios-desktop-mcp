import os
import sys
import platform
import subprocess
import json
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def setup_venv(base_dir):
    venv_dir = os.path.join(base_dir, "venv")
    if not os.path.exists(venv_dir):
        print("📦 Creando entorno virtual...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], cwd=base_dir, check=True)
    
    print("📦 Instalando dependencias...")
    pip_exe = os.path.join(venv_dir, "Scripts", "pip.exe") if platform.system() == "Windows" else os.path.join(venv_dir, "bin", "pip")
    subprocess.run([pip_exe, "install", "-r", "requirements.txt"], cwd=base_dir, check=True)
    
    python_exe = os.path.join(venv_dir, "Scripts", "python.exe") if platform.system() == "Windows" else os.path.join(venv_dir, "bin", "python")
    return python_exe

def update_json_config(file_path, server_config):
    path = Path(file_path)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        config = {"mcpServers": {}}
    else:
        try:
            with open(path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except json.JSONDecodeError:
            config = {"mcpServers": {}}

    if "mcpServers" not in config:
        config["mcpServers"] = {}

    config["mcpServers"]["arkaios-desktop"] = server_config

    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
    print(f"✅ Configuración inyectada en: {file_path}")

def get_claude_desktop_path():
    sys_os = platform.system()
    if sys_os == "Windows":
        return os.path.expandvars(r"%APPDATA%\Claude\claude_desktop_config.json")
    elif sys_os == "Darwin":
        return os.path.expanduser("~/Library/Application Support/Claude/claude_desktop_config.json")
    else:
        # Not supported natively by Claude Desktop yet, but fallback
        return os.path.expanduser("~/.config/Claude/claude_desktop_config.json")

def get_cline_vscode_path():
    sys_os = platform.system()
    if sys_os == "Windows":
        return os.path.expandvars(r"%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json")
    elif sys_os == "Darwin":
        return os.path.expanduser("~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json")
    else:
        return os.path.expanduser("~/.config/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json")

def main():
    print("🚀 Iniciando Instalador Universal de ARKAIOS Addon...")
    base_dir = os.path.abspath(os.path.dirname(__file__))
    
    # 1. Setup Venv
    python_exe = setup_venv(base_dir)
    server_script = os.path.join(base_dir, "server.py")

    # The base MCP config
    server_config = {
        "command": python_exe,
        "args": [server_script]
    }

    # 2. Inject Claude Desktop
    claude_path = get_claude_desktop_path()
    server_config["env"] = {"ARKAIOS_CLIENT": "claude"}
    update_json_config(claude_path, server_config)

    # 3. Inject VS Code Cline
    cline_path = get_cline_vscode_path()
    server_config["env"] = {"ARKAIOS_CLIENT": "vscode"}
    update_json_config(cline_path, server_config)

    print("🎉 ¡Instalación completada! El Addon ya está disponible en tus agentes IA.")

if __name__ == "__main__":
    main()
