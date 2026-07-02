# Configuración de Servidor MCP para GitHub Copilot

Hola, Copilot. Como asistente de IA, tienes soporte para usar servidores locales a través del Model Context Protocol (MCP) en VS Code.

El usuario quiere conectarte a su servidor local de control de escritorio (ARKAIOS). Tu objetivo es ayudarle a configurar el archivo `mcp.json` (o las configuraciones de MCP de VS Code) para que adquieras estas herramientas.

**Configuración requerida:**
Debes agregar lo siguiente a los servidores MCP de VS Code:

```json
{
  "mcpServers": {
    "arkaios-desktop": {
      "command": "C:\\ARKAIOS\\Agente Autonomo MVP\\mcp_server\\venv\\Scripts\\python.exe",
      "args": ["C:\\ARKAIOS\\Agente Autonomo MVP\\mcp_server\\server.py"],
      "env": {
        "ARKAIOS_CLIENT": "copilot"
      }
    }
  }
}
```

Por favor, lee esta configuración e indícale al usuario si puedes agregarla automáticamente o pídele que abra los ajustes de "Copilot MCP Servers" en la paleta de comandos de VS Code para pegarla.
